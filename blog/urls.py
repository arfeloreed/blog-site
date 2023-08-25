from django.urls import path
from . import views


# all urls
urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("posts", views.AllPostsView.as_view(), name="all-posts"),
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
]
