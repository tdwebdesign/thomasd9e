from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "post_status"]
        widgets = {
            "slug": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    # Using CKEditor for the content field
    content = forms.CharField(widget=CKEditorWidget())


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
