from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from blogs.models import Posts,Categories,ForbiddenWords
from django.http import HttpResponseRedirect
class post_form(forms.ModelForm):
	class Meta:
		model = Posts
		fields = ('title','picture','content','category')
        

class category_form(forms.ModelForm):
  class Meta:
    model = Categories
    fields = ('title',)
    widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
class ForbiddenWordForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
	class Meta:
		model = ForbiddenWords
		fields = ('title',)