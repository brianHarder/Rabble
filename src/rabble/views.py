from django.shortcuts import render
from .models import SubRabble, Post
from django.shortcuts import get_object_or_404
from .forms import PostForm

def index(request):
    context = {
        'subrabbles': SubRabble.objects.all()
    }
    return render(request, "rabble/index.html", context)

def profile(request):
    return render(request, "rabble/profile.html")

def subrabble_detail(request, subrabble_community_id):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    posts = Post.objects.filter(subrabble_id=subrabble)

    context = {
        'subrabble': subrabble,
        'posts': posts
    }

    return render(request, "rabble/subrabble_detail.html", context)

def post_detail(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    context = {
        'subrabble': subrabble,
        'post': post
    }

    return render(request, "rabble/post_detail.html", context)

def post_create(request, subrabble_community_id):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    form = PostForm()

    context = {
        'subrabble': subrabble,
        'form': form
    }

    return render(request, "rabble/post_form.html", context)

def post_edit(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)
    form = PostForm(instance=post)

    context = {
        'subrabble': subrabble,
        'form': form
    }

    return render(request, "rabble/post_form.html", context)
