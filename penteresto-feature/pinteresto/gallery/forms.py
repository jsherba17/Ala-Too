from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        new_title = self.cleaned_data['title'].lower()

        if new_title == 'create':
            raise ValidationError('Название тега не может быть "create"')
        if Tag.objects.filter(title__iexact=new_title).count():
            raise ValidationError(f'Тег {new_title} уже существует')
        return new_title
