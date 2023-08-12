from django.urls import path
from . import views


# all urls
urlpatterns = [
    path("", views.index, name="home"),
    path("posts", views.posts, name="all-posts"),
    path("posts/<slug:slug>", views.post, name="post"),
]
