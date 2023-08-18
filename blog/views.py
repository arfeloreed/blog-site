from django.shortcuts import render, get_object_or_404
from .models import Post


# variable
all_posts = Post.objects.all().order_by("-date")


# Create your views here.
def index(request):
    latest_posts = all_posts[:3]
    return render(
        request,
        "blog/index.html",
        {
            "posts": latest_posts,
        },
    )


def posts(request):
    return render(
        request,
        "blog/posts.html",
        {
            "posts": all_posts,
        },
    )


def post(request, slug):
    selected_post = get_object_or_404(Post, slug=slug)
    return render(
        request,
        "blog/post.html",
        {
            "post": selected_post,
            "tags": selected_post.tags.all(),
        },
    )
