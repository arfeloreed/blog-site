from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import CommentForm
from .models import Post

# variable
all_posts = Post.objects.all().order_by("-date")


# Create your views here.
# def index(request):
#     latest_posts = all_posts[:3]
#     return render(
#         request,
#         "blog/index.html",
#         {
#             "posts": latest_posts,
#         },
#     )


# using ListView for rendering index page
class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"
    # set how the order of how the objects should be viewed
    ordering = ["-date"]

    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     latest_posts = base_query.all().order_by("-date")[:3]
    #     return latest_posts

    def get_queryset(self):
        base_query = super().get_queryset()
        latest_posts = base_query[:3]
        return latest_posts


# using ListView for rendering the all posts page
# def posts(request):
#     return render(
#         request,
#         "blog/posts.html",
#         {
#             "posts": all_posts,
#         },
#     )

class AllPostsView(ListView):
    template_name = "blog/posts.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]


# using DetailView for rendering the post detail view
# def post(request, slug):
#     selected_post = get_object_or_404(Post, slug=slug)
#     return render(
#         request,
#         "blog/post.html",
#         {
#             "post": selected_post,
#             "tags": selected_post.tags.all(),
#         },
#     )

# class PostDetailView(DetailView):
#     template_name = "blog/post.html"
#     model = Post

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tags"] = self.object.tags.all()
#         context["form"] = CommentForm()
#         return context

# rendering indexView using View class based for get and post request
class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_read_later = post_id in stored_posts
        else:
            is_read_later = False

        return is_read_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "tags": post.tags.all(),
            "form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }

        return render(
            request,
            "blog/post.html",
            context,
        )

    def post(self, request, slug):
        comment = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment.is_valid():
            # linking the related post to the comment object
            comment = comment.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post", args=[slug]))

        context = {
            "post": post,
            "tags": post.tags.all(),
            "form": comment,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }

        return render(
            request,
            "blog/post.html",
            context,
        )


# view for read later
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(
            request,
            "blog/stored_posts.html",
            context,
        )

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        # check if user stored a post
        if stored_posts is None:
            stored_posts = []

        # get the id of the current post the user is in
        post_id = int(request.POST["post_id"])
        # check if the id exists in stored_post, if not append it on the list
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            # save or overwrite the stored_posts variable
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
