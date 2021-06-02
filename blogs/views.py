
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import post_form, category_form
from .models import Users, Categories, Tags, Posts, Replies, Comments, ForbiddenWords
from .logger import log
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import send_mail
import os



# Create your views here.

def say_dashboard(request):
    return render(request, 'dashboard/base.html',{})


def say_blogs(request):
    return render(request, 'user/blogs.html', {})


def blog_detail(request, id):
    post = Posts.objects.get(id = id)
    comments = Comments.objects.filter(post=post)
    context = {
        "post":post,
        "comments": comments,
    }
    return render(request, 'user/post-details.html', context)


# add category
def new_category(request):
    form = category_form()
    if request.method == 'POST':
        form = category_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/all')

    context = {'ct_form': form}
    return render(request, 'dashboard/newcategory.html', context)


# edit category
def edit_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    form = category_form(instance=category)
    if request.method == 'POST':
        form = category_form(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/all')

    context = {'ct_form': form}
    return render(request, 'dashboard/newcategory.html', context)


# delete
def delete_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    category.delete()
    return HttpResponseRedirect('/dashboard/all')


# get all category
def getAllCategory(request):
    all_category = Categories.objects.all()
    context = {'categories': all_category}
    return render(request, 'dashboard/category.html', context)




#register
def register(request):
    """this custom login view does the following:
    1- checks if request comes from an already logged in user so it redirects him to hompage again
    2- check if the method is post and then the submitted form is valid"""
    

    if(not request.user.is_authenticated):
        if request.method == "POST":
            user_form = RegistrationForm(request.POST)
            # get the form and the upladed files
            # profile_form = ProfileForm(request.POST, request.FILES)
            if user_form.is_valid():
                user = user_form.save()  # save the user into database and return it
                # get the profile of the created user
                # profile = Profile.objects.get(user=user)
                # get the uplloaded picture if any
                file = request.FILES.get("profile_pic")
                # if(file != None):
                #     profile.profile_pic = file  # add the provided pic to that user profile
                # profile.bio = request.POST["bio"]
                # profile.save()  # save the updates to user profile
                # log(profile.profile_pic.url)
                log("created a new user successfully with username: " +
                    user.username)  # for debugging purposes
                user = authenticate(
                    username=request.POST["username"], password=request.POST["password1"])
                if user is not None:
                    login(request, user)
                    try:
                        send_mail('Welcome to our blog', 'Django Blog team welcomes you to our blog .',
                                  'ahmedelbaiomy40@gmail.com', [user.email], fail_silently=False,)
                    except Exception as ex:
                        log("couldn't send email message"+str(ex))

                    # redirect to user profile page
                    return HttpResponseRedirect("/user/profile")
                else:
                    log("cannot login from registration form")
            else:
                log("invalid registration form")  # for debugging purposes
        else:
            user_form = RegistrationForm()
            # profile_form = ProfileForm()
        context = {"user_form": user_form}
        # context = {"user_form": user_form, "profile_form": profile_form}
        return render(request, 'user/register.html', context)
    else:
        return HttpResponseRedirect("/")

import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import post_form, category_form,ForbiddenWordForm
from .models import Users, Categories, Tags, Posts, Replies, Comments, ForbiddenWords

# Create your views here.


def say_dashboard(request):
    return render(request, 'dashboard/base.html', {})


def say_blogs(request):
    return render(request, 'user/blogs.html', {})


def blog_detail(request, id):
    post = Posts.objects.get(id=id)
    comments = Comments.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
    }
    return render(request, 'user/post-details.html', context)


# add category
def new_category(request):
    form = category_form()
    if request.method == 'POST':
        form = category_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/all/')

    context = {'ct_form': form}
    return render(request, 'dashboard/newcategory.html', context)


# edit category
def edit_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    form = category_form(instance=category)
    if request.method == 'POST':
        form = category_form(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/all/')

    context = {'ct_form': form}
    return render(request, 'dashboard/newcategory.html', context)


# delete
def delete_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    category.delete()
    return HttpResponseRedirect('/all/')


# get all category
def getAllCategory(request):
    all_category = Categories.objects.all()
    context = {'categories': all_category}
    return render(request, 'dashboard/category.html', context)

#add forbiden word
def add_forbiden_word(request):
    form = ForbiddenWordForm()
    if request.method == 'POST':
        form = ForbiddenWordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/allforbidden/')
    else:
        context = {"pt_form": form}
        return render(request,"dashboard/newforbiden.html",context)

#delete forbidden word 
def delete_forbiden_word(request, word_id):
   title = ForbiddenWords.objects.get(id=word_id)
   title.delete()
   return HttpResponseRedirect('/allforbidden/')

# get all forbiden word
def getAllWord(request):
    all_word= ForbiddenWords.objects.all()
    context = {'words': all_word}
    return render(request, 'dashboard/allword.html', context)

# edit word
def edit_forbiden_word(request, word_id):
    word = ForbiddenWords.objects.get(id=word_id)
    form = ForbiddenWordForm(instance=word)
    if request.method == 'POST':
        form = ForbiddenWordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/allforbidden/')

    context = {'pt_form': form}
    return render(request, 'dashboard/newforbiden.html', context)

#take comment text to be replaced with the original comment on post
def check_forbidden_words_in_comment(request, content):
    content_arr = content.split(",")
    all_forbidden_words = ForbiddenWords.objects.all()
    for word in all_forbidden_words:
        replaced=""
        if content.find(word.title):
            for c in word.title:
                replaced+="*"
            content= content.replace(word.title,replaced)

    return HttpResponseRedirect('/forbidden_words/')


def check_profanity(content):
    filtered = ''
    first_word = True
    for word in content.split():
        if not first_word:
            filtered += ' '
        first_word = False
        if ForbiddenWords.objects.filter(title = word.lower()):
            filtered += ('*' * len(word))
        else:
            filtered += word
    return filtered

# new post
def new_post(request):
    form = post_form()
    # user_id = request.user.id
    # print(user_id)
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        post = form.save(commit=False)
        print(form)
        # post.user_id = int(user_id)
        # print(form)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect(
                '#')

    context = {'p_form': form}
    return render(request, 'dashboard/newpost.html', context)
