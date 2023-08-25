from django.contrib import admin
from .models import Post, Author, Tag, Comment


# manipulating the admin display
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "author")
    list_filter = ("author", "tags", "date")
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "post")


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
