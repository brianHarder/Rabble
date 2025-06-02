from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Rabble, SubRabble, Post, Comment
from .forms import PostForm, CommentForm, SubRabbleForm, UserRegistrationForm

@login_required
def profile(request):
    return render(request, "rabble/profile.html")

@login_required
def index(request):
    context = {
        'rabbles': Rabble.objects.all()
    }
    return render(request, "rabble/index.html", context)

@login_required
def rabble_detail(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabbles = SubRabble.objects.filter(rabble_id=rabble)
    
    context = {
        'rabble': rabble,
        'subrabbles': subrabbles
    }
    return render(request, "rabble/rabble_detail.html", context)

@login_required
def subrabble_create(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)

    if request.method == "POST":
        form = SubRabbleForm(request.POST)
        if form.is_valid():
            subrabble = form.save(commit=False)
            subrabble.rabble_id = rabble
            subrabble.user_id = request.user
            subrabble.save()
            return redirect("subrabble-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id)
    else:
        form = SubRabbleForm(rabble=rabble)
    
    context = {
        'form': form,
        'rabble': rabble
    }
    
    return render(request, "rabble/subrabble_form.html", context)

@login_required
def subrabble_detail(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    posts = Post.objects.filter(subrabble_id=subrabble)

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'posts': posts
    }

    return render(request, "rabble/subrabble_detail.html", context)

@login_required
def subrabble_edit(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)

    if request.method == "POST":
        form = SubRabbleForm(request.POST, instance=subrabble)
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

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'post': post,
        'liked': liked
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
            return redirect("post-detail", community_id=rabble.community_id, subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'rabble': rabble,
        'subrabble': subrabble,
        'form': form
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
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
