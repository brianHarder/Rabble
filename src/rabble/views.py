from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import Rabble, SubRabble, Post, Comment, User
from .forms import PostForm, CommentForm, SubRabbleForm, UserRegistrationForm, CustomLoginForm, RabbleForm, ForgotPasswordForm, ProfileEditForm
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import PostAnalysisService
import asyncio
from .models import PostRelationship
from rest_framework import status, viewsets
from django.db.models import Q
from django.core.cache import cache
import hashlib
import json

def get_posts_hash(posts):
    post_data = sorted([(post.id, post.title, post.body) for post in posts], key=lambda x: x[0])
    return hashlib.md5(json.dumps(post_data).encode()).hexdigest()

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Check if we should reset the profile picture
            if request.POST.get('reset_profile_picture'):
                request.user.profile_picture = 'images/default.png'
                request.user.save()
                messages.success(request, 'Your profile picture has been reset to default.')
                return redirect('profile')
            
            # Check if password is being changed
            if form.cleaned_data.get('new_password'):
                # Update password without logging out
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                # Update the session to prevent logout
                update_session_auth_hash(request, request.user)
            else:
                # Regular profile update
                form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, "rabble/profile.html", {
        'form': form,
        'user': request.user
    })

@login_required
def index(request):
    context = {
        'rabbles': Rabble.objects.all()
    }
    return render(request, "rabble/index.html", context)

@login_required
def rabble_detail(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabbles = SubRabble.objects.filter(rabble_id=rabble).filter(
        models.Q(private=False) | models.Q(members=request.user)
    ).distinct()
    
    context = {
        'rabble': rabble,
        'subrabbles': subrabbles
    }
    return render(request, "rabble/rabble_detail.html", context)

@login_required
def rabble_create(request):
    if request.method == "POST":
        form = RabbleForm(request.POST)
        if form.is_valid():
            rabble = form.save(commit=False)
            rabble.owner = request.user
            rabble.save()
            form.save_m2m()
            # Add the owner to the members list if not already added
            if request.user not in rabble.members.all():
                rabble.members.add(request.user)
            return redirect("rabble-detail", community_id=rabble.community_id)
    else:
        form = RabbleForm()
        form.current_user = request.user
    
    return render(request, "rabble/rabble_form.html", {'form': form})

@login_required
def rabble_edit(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    
    if request.user != rabble.owner:
        return HttpResponseForbidden("You cannot edit this Rabble.")

    if request.method == "POST":
        form = RabbleForm(request.POST, instance=rabble)
        if form.is_valid():
            form.save()
            return redirect("rabble-detail", community_id=rabble.community_id)
    else:
        form = RabbleForm(instance=rabble)
    
    return render(request, "rabble/rabble_form.html", {'form': form, 'rabble': rabble})

@login_required
def rabble_delete(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    
    if request.user != rabble.owner:
        return HttpResponseForbidden("You cannot delete this Rabble.")

    if request.method == "POST":
        rabble.delete()
        return redirect("index")

    return render(request, "rabble/rabble_delete.html", {'rabble': rabble})

@login_required
def subrabble_create(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)

    if request.method == "POST":
        form = SubRabbleForm(request.POST, rabble=rabble)
        if form.is_valid():
            subrabble = form.save(commit=False)
            subrabble.rabble_id = rabble
            subrabble.user_id = request.user
            subrabble.save()
            form.save_m2m()  # Save the many-to-many relationships
            # Add the creator to the members list if not already added
            if request.user not in subrabble.members.all():
                subrabble.members.add(request.user)
            return redirect("subrabble-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id)
    else:
        form = SubRabbleForm(rabble=rabble)
        form.current_user = request.user
    
    context = {
        'form': form,
        'rabble': rabble
    }
    
    return render(request, "rabble/subrabble_form.html", context)

@login_required
def subrabble_detail(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
   
    posts = Post.objects.filter(subrabble_id=subrabble).order_by('-id')
    posts_hash_key = f'subrabble_posts_hash_{subrabble.id}'
    current_posts_hash = get_posts_hash(posts)
    
    # Check if posts/content has changed
    cached_posts_hash = cache.get(posts_hash_key)
    should_run_analysis = (cached_posts_hash is None or cached_posts_hash != current_posts_hash)
    
    if should_run_analysis and posts.exists():
        # Create event loop for async processing
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            service = PostAnalysisService()
            loop.run_until_complete(service.analyze_all_posts(subrabble.id))
            
            # Update the posts hash in cache after successful analysis
            cache.set(posts_hash_key, current_posts_hash, timeout=3600)
            
        except Exception as e:
            print(f"DEBUG: subrabble_detail - Error during analysis: {e}")
            cache.delete(posts_hash_key)
        finally:
            loop.close()

    # Always regenerate posts_with_relationships from fresh database data
    posts_with_relationships = []
    for post in posts:
        relationships = PostRelationship.objects.filter(
            Q(source_post=post) | Q(target_post=post)
        ).select_related('source_post', 'target_post')
        
        outgoing = []
        incoming = []
        
        for rel in relationships:
            if rel.source_post == post:
                outgoing.append({
                    'relationship_type': rel.relationship_type,
                    'target_post_id': rel.target_post.id,
                    'target_post_title': rel.target_post.title
                })
            else:
                incoming.append({
                    'relationship_type': rel.relationship_type,
                    'source_post_id': rel.source_post.id,
                    'source_post_title': rel.source_post.title
                })
        
        # Serialize the post object to a dict
        post_dict = {
            'pk': post.pk,
            'title': post.title,
            'body': post.body,
            'anonymous': post.anonymous,
            'rabble_id': post.subrabble_id.rabble_id.community_id if hasattr(post.subrabble_id, 'rabble_id') and hasattr(post.subrabble_id.rabble_id, 'community_id') else None,
            'subrabble_id': post.subrabble_id.subrabble_community_id if hasattr(post.subrabble_id, 'subrabble_community_id') else None,
            'user_id': {
                'username': post.user_id.username if post.user_id else None
            },
            'post_likes': list(post.post_likes.values_list('pk', flat=True)) if hasattr(post, 'post_likes') else [],
            'comment_set': list(post.comment_set.values_list('pk', flat=True)) if hasattr(post, 'comment_set') else [],
        }

        posts_with_relationships.append({
            'post': post_dict,
            'outgoing': outgoing,
            'incoming': incoming
        })
    
    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'posts_with_relationships': posts_with_relationships,
        'posts_with_relationships_json': json.dumps(posts_with_relationships),
    }

    return render(request, "rabble/subrabble_detail.html", context)

@login_required
def subrabble_edit(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)

    if request.user != subrabble.user_id:
        return HttpResponseForbidden("You cannot edit this SubRabble.")

    if request.method == "POST":
        form = SubRabbleForm(request.POST, instance=subrabble, rabble=rabble)
        if form.is_valid():
            form.save()
            return redirect("subrabble-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id)
    else:
        form = SubRabbleForm(instance=subrabble, rabble=rabble)
    
    context = {
        'form': form,
        'subrabble': subrabble,
        'rabble': rabble
    }

    return render(request, "rabble/subrabble_form.html", context)

@login_required
def subrabble_delete(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)

    if request.method == "POST":
        subrabble.delete()
        return redirect("rabble-detail", community_id=rabble.community_id)

    context = {
        'subrabble': subrabble,
        'rabble': rabble
    }

    return render(request, "rabble/subrabble_delete.html", context)

@login_required
def post_detail(request, community_id, subrabble_community_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)
    liked = False
    if request.user.is_authenticated:
        liked = request.user in post.post_likes.all()

    # Get comments with like information
    comments = post.comment_set.all()
    if request.user.is_authenticated:
        for comment in comments:
            comment.user_has_liked = request.user in comment.comment_likes.all()

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post,
        'liked': liked,
        'comments': comments
    }

    return render(request, "rabble/post_detail.html", context)

@login_required
def post_create(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.subrabble_id = subrabble
            post.save()
            return redirect("post-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    else:
        form = PostForm()

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'form': form
    }

    return render(request, "rabble/post_form.html", context)

@login_required
def post_edit(request, community_id, subrabble_community_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    if request.user != post.user_id:
        return HttpResponseForbidden("You cannot edit other people's posts.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("subrabble-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id)
    else:
        form = PostForm(instance=post)

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'form': form,
        'post': post
    }
    return render(request, "rabble/post_form.html", context)

@login_required
def post_delete(request, community_id, subrabble_community_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    if request.user != post.user_id:
        return HttpResponseForbidden("You cannot delete other people's posts.")

    if request.method == "POST":
        post.delete()
        return redirect("subrabble-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id)

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post
    }
    return render(request, "rabble/post_delete.html", context)

@login_required
def comment_create(request, community_id, subrabble_community_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = request.user
            comment.post_id = post
            comment.save()
            return redirect("post-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post,
        'form': form
    }

    return render(request, "rabble/comment_form.html", context)

@login_required
def comment_edit(request, community_id, subrabble_community_id, post_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=post_id, subrabble_id=subrabble)
    comment = get_object_or_404(Comment, pk=pk, post_id=post)

    if request.user != comment.user_id:
        return HttpResponseForbidden("You cannot edit other people's comments.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("post-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post,
        'form': form
    }
    return render(request, "rabble/comment_form.html", context)

@login_required
def comment_delete(request, community_id, subrabble_community_id, post_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=post_id, subrabble_id=subrabble)
    comment = get_object_or_404(Comment, pk=pk, post_id=post)

    if request.user != comment.user_id:
        return HttpResponseForbidden("You cannot delete other users' comments.")
    
    if request.method == "POST":
        comment.delete()
        return redirect("post-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    
    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post,
        'comment': comment
    }
    return render(request, "rabble/comment_delete.html", context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            
            user = User.objects.get(username=username, email=email)
            user.set_password(new_password)
            user.save()
            
            messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
            return redirect('login')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'rabble/forgot_password.html', {'form': form})

class PostViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def analyze_relationships(self, request):
        subrabble_id = request.data.get('subrabble_id')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            service = PostAnalysisService()
            loop.run_until_complete(service.analyze_all_posts(subrabble_id))
            return Response({'status': 'analysis completed'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            loop.close()

    @action(detail=True, methods=['get'])
    def relationships(self, request, pk=None):
        post = self.get_object()
        
        outgoing = PostRelationship.objects.filter(source_post=post)
        incoming = PostRelationship.objects.filter(target_post=post)
        
        data = {
            'outgoing': [{
                'target_post_id': rel.target_post.id,
                'relationship_type': rel.relationship_type
            } for rel in outgoing],
            'incoming': [{
                'source_post_id': rel.source_post.id,
                'relationship_type': rel.relationship_type
            } for rel in incoming]
        }
        
        return Response(data)
