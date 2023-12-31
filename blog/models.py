from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.
# models for tag objects
class Tag(models.Model):
    caption = models.CharField(max_length=70)

    def __str__(self):
        return self.caption


# models for author objects
class Author(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email_add = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


# model for all posts objects
class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to="posts_images")
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    excerpt = models.CharField(max_length=200)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


# model for comment objects
class Comment(models.Model):
    username = models.CharField(max_length=120)
    email = models.EmailField()
    comment = models.TextField(max_length=480)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
