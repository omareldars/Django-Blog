from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from blogs.models import Posts,Categories
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
