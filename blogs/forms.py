from django.contrib.auth.forms import AuthenticationForm
from django import forms
from blogs.models import Posts, Categories
from django.http import HttpResponseRedirect


class post_form(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('title', 'picture', 'content', 'category', 'author', 'tag')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'custom-select'}),
            'tag': forms.Select(attrs={'class': 'custom-select'}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file'}),

            'category': forms.Select(attrs={'class': 'custom-select'}),
        }


class category_form(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),

        }
