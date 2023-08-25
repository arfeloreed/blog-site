from django import forms
from .models import Comment


# forms are written below
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ["post",]
        labels = {
            "comment": "Your comment",
        }
