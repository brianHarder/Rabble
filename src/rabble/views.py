from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import SubRabble, Post, Comment
from .forms import PostForm, CommentForm

@login_required
def index(request):
    context = {
        'subrabbles': SubRabble.objects.all()
    }
    return render(request, "rabble/index.html", context)

@login_required
def profile(request):
    return render(request, "rabble/profile.html")

@login_required
def subrabble_detail(request, subrabble_community_id):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    posts = Post.objects.filter(subrabble_id=subrabble)

    context = {
        'subrabble': subrabble,
        'posts': posts
    }

    return render(request, "rabble/subrabble_detail.html", context)

@login_required
def subrabble_create():
    return

@login_required
def subrabble_edit():
    return

@login_required
def subrabble_delete():
    return

@login_required
def post_detail(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    context = {
        'subrabble': subrabble,
        'post': post
    }

    return render(request, "rabble/post_detail.html", context)

@login_required
def post_create(request, subrabble_community_id):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.subrabble_id = subrabble
            post.save()
            return redirect("post-detail", subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    else:
        form = PostForm()

    context = {
        'subrabble': subrabble,
        'form': form
    }

    return render(request, "rabble/post_form.html", context)

@login_required
def post_edit(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    if request.user != post.user_id:
        return HttpResponseForbidden("You cannot edit other people's posts.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post-detail", subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'subrabble': subrabble,
        'form': form
    }
    return render(request, "rabble/post_form.html", context)

@login_required
def post_delete(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    if request.user != post.user_id:
        return HttpResponseForbidden("You cannot delete other people's posts.")

    if request.method == "POST":
        post.delete()
        return redirect("subrabble-detail", subrabble_community_id=subrabble.subrabble_community_id)

    context = {
        'subrabble': subrabble,
        'post': post
    }
    return render(request, "rabble/post_delete.html", context)

@login_required
def comment_create(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = request.user
            comment.post_id = post
            comment.save()
            return redirect("post-detail", subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)

    context = {
        'subrabble': subrabble,
        'post': post,
        'form': form
    }

    return render(request, "rabble/comment_form.html", context)

@login_required
def comment_edit(request, subrabble_community_id, post_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=post_id, subrabble_id=subrabble)
    comment = get_object_or_404(Comment, pk=pk, post_id=post)

    if request.user != comment.user_id:
        return HttpResponseForbidden("You cannot edit other people's comments.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("post-detail", subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        'subrabble': subrabble,
        'post': post,
        'form': form
    }
    return render(request, "rabble/comment_form.html", context)

@login_required
def comment_delete(request, subrabble_community_id, post_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=post_id, subrabble_id=subrabble)
    comment = get_object_or_404(Comment, pk=pk, post_id=post)

    if request.user != comment.user_id:
        return HttpResponseForbidden("You cannot delete other users' comments.")
    
    if request.method == "POST":
        comment.delete()
        return redirect("post-detail", subrabble_community_id=subrabble.subrabble_community_id, pk=post.pk)
    
    context = {
        'subrabble': subrabble,
        'post': post,
    }
    return render(request, "rabble/comment_delete.html", context)
