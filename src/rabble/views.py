from django.shortcuts import render
from .models import SubRabble, Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

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
    form = PostForm(instance=post)

    if request.user != post.user_id:
        return HttpResponseForbidden("You cannot edit other users' posts.")

    context = {
        'subrabble': subrabble,
        'form': form
    }

    return render(request, "rabble/post_form.html", context)
