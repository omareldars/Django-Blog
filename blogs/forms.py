from django import forms
from blogs.models import Posts,Categories,ForbiddenWords,Tags
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm ,UsernameField , PasswordChangeForm
from django.http import  HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm



class post_form(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('title', 'picture', 'content', 'author', 'tag', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'custom-select'}),
            'tag': forms.Select(attrs={'class': 'custom-select'}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file'}),
            # 'category': forms.CheckboxSelectMultiple(attrs={'class': 'select', 'multiple':True,})
            'category': forms.Select(attrs={'class':'custom-select'}),
        }
        # category = forms.ModelMultipleChoiceField(
		# 	queryset=Categories.objects.all(),
		# 	widget=forms.CheckboxSelectMultiple
		# )



class category_form(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),

        }


# Registration Form

class RegistrationForm(UserCreationForm):

    """custom registration form inherits from UserCreationForm provided by django authentication
        forms . email field exists in the database already"""
        
    email = forms.EmailField(required=True,max_length=100,
                            widget=forms.EmailInput(attrs={'class': 'input100' ,'placeholder': 'email@example.com'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100','placeholder': 'Enter new password'}),
    label="password",help_text="at least 8 charachters , numbers , symbols or better mix them")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100','placeholder': 'Confirm your password'}),
    label="confirm password")
    class Meta:
        model = User
        fields =['username','email','first_name' , 'last_name' ]
        widgets = {
			'username' : forms.TextInput(attrs={'class': 'input100','placeholder': 'Enter username'}),
            'first_name':forms.TextInput(attrs={'class': 'input100' ,'placeholder': 'Enter your first name'}),
            'last_name':forms.TextInput(attrs={'class': 'input100','placeholder': 'Enter your last name'}),
		}
    def clean(self):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("username already used before.. try another one")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already used before.. try another one")
        return self.cleaned_data


class ForbiddenWordForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
	class Meta:
		model = ForbiddenWords
		fields = ('title',)

class TagForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
	class Meta:
		model = Tags
		fields = ('title',)
