from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """На основе модели Post создаем класс формы с полями text, group"""
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
