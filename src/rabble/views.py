from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import Rabble, SubRabble, Post, Comment, User, CommentLike
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
from django.urls import reverse
from .view_helpers import serialize_form, page_context


def get_posts_hash(posts):
    post_data = sorted([(post.id, post.title, post.body) for post in posts], key=lambda x: x[0])
    return hashlib.md5(json.dumps(post_data).encode()).hexdigest()


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if request.POST.get('reset_profile_picture'):
                request.user.profile_picture = 'images/default.png'
                request.user.save()
                messages.success(request, 'Your profile picture has been reset to default.')
                return redirect('profile')

            if form.cleaned_data.get('new_password'):
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
            else:
                form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)

    is_default = request.user.profile_picture.name == 'images/default.png'
    from django.templatetags.static import static as static_url
    if is_default:
        pic_url = static_url('images/default.png')
    else:
        pic_url = request.user.profile_picture.url

    msg_list = []
    storage = messages.get_messages(request)
    for m in storage:
        msg_list.append({'text': str(m), 'tags': m.tags})

    page_data = page_context(request, {
        'form': serialize_form(form),
        'profile_picture_url': pic_url,
        'is_default_pic': is_default,
        'messages': msg_list,
        'index_url': reverse('index'),
    })

    return render(request, "rabble/profile.html", {
        'page_data': page_data,
    })


@login_required
def index(request):
    rabbles = Rabble.objects.all()
    page_data = page_context(request, {
        'rabbles': [
            {
                'community_id': r.community_id,
                'description': r.description,
                'private': r.private,
                'is_member': request.user in r.members.all(),
                'url': reverse('rabble-detail', args=[r.community_id]),
            }
            for r in rabbles
        ],
        'create_url': reverse('rabble-create'),
    })
    return render(request, "rabble/index.html", {'page_data': page_data})


@login_required
def rabble_detail(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabbles = SubRabble.objects.filter(rabble_id=rabble).filter(
        models.Q(private=False) | models.Q(members=request.user)
    ).distinct()

    page_data = page_context(request, {
        'rabble': {
            'community_id': rabble.community_id,
            'description': rabble.description,
        },
        'is_owner': request.user == rabble.owner,
        'subrabbles': [
            {
                'subrabble_community_id': sr.subrabble_community_id,
                'subrabble_name': sr.subrabble_name,
                'description': sr.description,
                'private': sr.private,
                'url': reverse('subrabble-detail', args=[community_id, sr.subrabble_community_id]),
            }
            for sr in subrabbles
        ],
        'edit_url': reverse('rabble-edit', args=[community_id]),
        'delete_url': reverse('rabble-delete', args=[community_id]),
        'create_subrabble_url': reverse('subrabble-create', args=[community_id]),
        'index_url': reverse('index'),
    })
    return render(request, "rabble/rabble_detail.html", {'page_data': page_data})


@login_required
def rabble_create(request):
    if request.method == "POST":
        form = RabbleForm(request.POST)
        if form.is_valid():
            rabble = form.save(commit=False)
            rabble.owner = request.user
            rabble.save()
            form.save_m2m()
            if request.user not in rabble.members.all():
                rabble.members.add(request.user)
            return redirect("rabble-detail", community_id=rabble.community_id)
    else:
        form = RabbleForm()
        form.current_user = request.user

    member_choices = [
        {'value': str(u.pk), 'label': str(u)}
        for u in User.objects.all()
    ]

    page_data = page_context(request, {
        'form': serialize_form(form),
        'member_choices': member_choices,
        'cancel_url': reverse('index'),
    })
    return render(request, "rabble/rabble_form.html", {'form': form, 'page_data': page_data})


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

    member_choices = [
        {'value': str(u.pk), 'label': str(u)}
        for u in User.objects.all()
    ]

    page_data = page_context(request, {
        'form': serialize_form(form),
        'member_choices': member_choices,
        'edit_url': reverse('api-rabble', args=[community_id]),
        'success_url': reverse('rabble-detail', args=[community_id]),
        'cancel_url': reverse('rabble-detail', args=[community_id]),
        'original_community_id': community_id,
    })
    return render(request, "rabble/rabble_form.html", {'form': form, 'rabble': rabble, 'page_data': page_data})


@login_required
def rabble_delete(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)

    if request.user != rabble.owner:
        return HttpResponseForbidden("You cannot delete this Rabble.")

    if request.method == "POST":
        rabble.delete()
        return redirect("index")

    page_data = page_context(request, {
        'heading': f'Are you sure you want to delete the community "{rabble.community_id}"?',
        'confirm_label': 'Delete',
        'cancel_url': reverse('rabble-detail', args=[community_id]),
    })
    return render(request, "rabble/rabble_delete.html", {'rabble': rabble, 'page_data': page_data})


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
            form.save_m2m()
            if request.user not in subrabble.members.all():
                subrabble.members.add(request.user)
            return redirect("subrabble-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id)
    else:
        form = SubRabbleForm(rabble=rabble)
        form.current_user = request.user

    member_choices = [
        {'value': str(u.pk), 'label': str(u)}
        for u in form.fields['members'].queryset
    ]

    page_data = page_context(request, {
        'form': serialize_form(form),
        'member_choices': member_choices,
        'cancel_url': reverse('rabble-detail', args=[community_id]),
    })

    return render(request, "rabble/subrabble_form.html", {'form': form, 'page_data': page_data})


@login_required
def subrabble_detail(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)

    posts = Post.objects.filter(subrabble_id=subrabble).order_by('-id')
    posts_hash_key = f'subrabble_posts_hash_{subrabble.id}'
    current_posts_hash = get_posts_hash(posts)

    cached_posts_hash = cache.get(posts_hash_key)
    should_run_analysis = (cached_posts_hash is None or cached_posts_hash != current_posts_hash)

    if should_run_analysis and posts.exists():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            service = PostAnalysisService()
            loop.run_until_complete(service.analyze_all_posts(subrabble.id))
            cache.set(posts_hash_key, current_posts_hash, timeout=3600)
        except Exception as e:
            print(f"DEBUG: subrabble_detail - Error during analysis: {e}")
            cache.delete(posts_hash_key)
        finally:
            loop.close()

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

    page_data = page_context(request, {
        'rabble_community_id': community_id,
        'subrabble': {
            'subrabble_community_id': subrabble.subrabble_community_id,
            'subrabble_name': subrabble.subrabble_name,
            'description': subrabble.description,
        },
        'is_owner': request.user == subrabble.user_id,
        'posts_with_relationships': posts_with_relationships,
        'back_url': reverse('rabble-detail', args=[community_id]),
        'edit_url': reverse('subrabble-edit', args=[community_id, subrabble_community_id]),
        'delete_url': reverse('subrabble-delete', args=[community_id, subrabble_community_id]),
        'new_post_url': reverse('post-create', args=[community_id, subrabble_community_id]),
    })

    return render(request, "rabble/subrabble_detail.html", {
        'subrabble': subrabble,
        'page_data': page_data,
    })


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

    member_choices = [
        {'value': str(u.pk), 'label': str(u)}
        for u in form.fields['members'].queryset
    ]

    page_data = page_context(request, {
        'form': serialize_form(form),
        'member_choices': member_choices,
        'edit_url': reverse('api-subrabble', args=[community_id, subrabble_community_id]),
        'success_url': reverse('subrabble-detail', args=[community_id, subrabble_community_id]),
        'cancel_url': reverse('subrabble-detail', args=[community_id, subrabble_community_id]),
        'original_community_id': subrabble_community_id,
    })

    return render(request, "rabble/subrabble_form.html", {
        'form': form,
        'subrabble': subrabble,
        'rabble': rabble,
        'page_data': page_data,
    })


@login_required
def subrabble_delete(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)

    if request.method == "POST":
        subrabble.delete()
        return redirect("rabble-detail", community_id=rabble.community_id)

    page_data = page_context(request, {
        'heading': f'Are you sure you want to delete !{subrabble.subrabble_community_id} — {subrabble.subrabble_name}?',
        'confirm_label': 'Delete Rabble',
        'cancel_url': reverse('subrabble-detail', args=[community_id, subrabble_community_id]),
    })

    return render(request, "rabble/subrabble_delete.html", {
        'subrabble': subrabble,
        'rabble': rabble,
        'page_data': page_data,
    })


@login_required
def post_detail(request, community_id, subrabble_community_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)
    liked = False
    if request.user.is_authenticated:
        liked = request.user in post.post_likes.all()

    comments_qs = post.comment_set.all()
    comments_data = []
    if request.user.is_authenticated:
        for comment in comments_qs:
            user_has_liked = CommentLike.objects.filter(user=request.user, comment=comment, is_dislike=False).exists()
            user_has_disliked = CommentLike.objects.filter(user=request.user, comment=comment, is_dislike=True).exists()
            like_count = CommentLike.objects.filter(comment=comment, is_dislike=False).count()
            dislike_count = CommentLike.objects.filter(comment=comment, is_dislike=True).count()

            comments_data.append({
                'pk': comment.pk,
                'text': comment.text,
                'anonymous': comment.anonymous,
                'username': comment.user_id.username if comment.user_id else 'unknown',
                'isOwner': request.user == comment.user_id,
                'userHasLiked': user_has_liked,
                'userHasDisliked': user_has_disliked,
                'likeCount': like_count,
                'dislikeCount': dislike_count,
                'likeUrl': reverse('comment-likes', args=[community_id, subrabble_community_id, pk, comment.pk]),
                'dislikeUrl': reverse('comment-dislikes', args=[community_id, subrabble_community_id, pk, comment.pk]),
                'editUrl': reverse('comment-edit', args=[community_id, subrabble_community_id, pk, comment.pk]),
                'deleteUrl': reverse('comment-delete', args=[community_id, subrabble_community_id, pk, comment.pk]),
            })

    page_data = page_context(request, {
        'subrabble_community_id': subrabble_community_id,
        'subrabble_name': subrabble.subrabble_name,
        'post': {
            'pk': post.pk,
            'title': post.title,
            'body': post.body,
            'anonymous': post.anonymous,
            'username': post.user_id.username if post.user_id else 'unknown',
            'liked': liked,
            'like_count': post.post_likes.count(),
            'comment_count': post.comment_set.count(),
            'is_owner': request.user == post.user_id,
            'like_url': reverse('post-likes', args=[community_id, subrabble_community_id, pk]),
            'edit_url': reverse('post-edit', args=[community_id, subrabble_community_id, pk]),
            'delete_url': reverse('post-delete', args=[community_id, subrabble_community_id, pk]),
        },
        'comments': comments_data,
        'back_url': reverse('subrabble-detail', args=[community_id, subrabble_community_id]),
        'new_comment_url': reverse('comment-create', args=[community_id, subrabble_community_id, pk]),
    })

    return render(request, "rabble/post_detail.html", {
        'post': post,
        'page_data': page_data,
    })


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

    page_data = page_context(request, {
        'form': serialize_form(form),
        'subrabble_community_id': subrabble_community_id,
        'allow_anonymous': subrabble.allow_anonymous,
        'cancel_url': reverse('subrabble-detail', args=[community_id, subrabble_community_id]),
    })

    return render(request, "rabble/post_form.html", {'form': form, 'page_data': page_data})


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

    page_data = page_context(request, {
        'form': serialize_form(form),
        'subrabble_community_id': subrabble_community_id,
        'allow_anonymous': subrabble.allow_anonymous,
        'edit_url': reverse('api-post-editor', args=[community_id, subrabble_community_id, pk]),
        'success_url': reverse('post-detail', args=[community_id, subrabble_community_id, pk]),
        'cancel_url': reverse('post-detail', args=[community_id, subrabble_community_id, pk]),
    })

    return render(request, "rabble/post_form.html", {
        'form': form,
        'post': post,
        'page_data': page_data,
    })


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

    page_data = page_context(request, {
        'heading': 'Are you sure you want to delete this post?',
        'details': [
            f'<strong>Title:</strong> {post.title or "(No Title)"}',
            f'<strong>Body:</strong> {post.body}',
        ],
        'confirm_label': 'Yes, delete',
        'cancel_url': reverse('post-detail', args=[community_id, subrabble_community_id, pk]),
    })

    return render(request, "rabble/post_delete.html", {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post,
        'page_data': page_data,
    })


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

    page_data = page_context(request, {
        'form': serialize_form(form),
        'post_title': post.title,
        'allow_anonymous': subrabble.allow_anonymous,
        'cancel_url': reverse('post-detail', args=[community_id, subrabble_community_id, pk]),
    })

    return render(request, "rabble/comment_form.html", {'form': form, 'page_data': page_data})


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

    page_data = page_context(request, {
        'form': serialize_form(form),
        'post_title': post.title,
        'allow_anonymous': subrabble.allow_anonymous,
        'edit_url': reverse('api-comment-editor', args=[community_id, subrabble_community_id, post_id, pk]),
        'success_url': reverse('post-detail', args=[community_id, subrabble_community_id, post_id]),
        'cancel_url': reverse('post-detail', args=[community_id, subrabble_community_id, post_id]),
    })

    return render(request, "rabble/comment_form.html", {'form': form, 'page_data': page_data})


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

    page_data = page_context(request, {
        'heading': 'Are you sure you want to delete this commment?',
        'details': [
            f'<strong>Body:</strong> {comment.text}',
        ],
        'confirm_label': 'Yes, delete',
        'cancel_url': reverse('post-detail', args=[community_id, subrabble_community_id, post_id]),
    })

    return render(request, "rabble/comment_delete.html", {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post,
        'comment': comment,
        'page_data': page_data,
    })


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    from django.templatetags.static import static as static_url
    page_data = page_context(request, {
        'form': serialize_form(form),
        'default_profile_pic': static_url('images/default.png'),
        'login_url': reverse('login'),
    })

    return render(request, 'registration/register.html', {'form': form, 'page_data': page_data})


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

    page_data = page_context(request, {
        'form': serialize_form(form),
        'register_url': reverse('register'),
        'forgot_password_url': reverse('forgot-password'),
    })

    return render(request, 'registration/login.html', {'form': form, 'page_data': page_data})


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

    page_data = page_context(request, {
        'form': serialize_form(form),
        'login_url': reverse('login'),
    })

    return render(request, 'rabble/forgot_password.html', {'form': form, 'page_data': page_data})


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
