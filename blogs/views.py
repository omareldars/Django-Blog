import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import post_form, category_form, ForbiddenWordForm,TagForm, RegistrationForm,LoginForm,ProfileForm
from .logger import log
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .util_funcs import isLocked
import os
from .models import Categories, Tags, Posts, Replies, Comments, ForbiddenWords, Profile
from .util_funcs import delete_profile_pic


#register
def register(request):
    """this custom login view does the following:
    1- checks if request comes from an already logged in user so it redirects him to hompage again
    2- check if the method is post and then the submitted form is valid"""
    
    print(request.POST)
    if( not request.user.is_authenticated):
        if request.method == "POST":
            user_form = RegistrationForm(request.POST)
            print(user_form.is_valid())

            # get the form and the upladed files
            profile_form = ProfileForm(request.POST, request.FILES)
            print("profile_form_data--->",profile_form.data,profile_form.files)
            if user_form.is_valid():
                user = user_form.save()  # save the user into database and return it
                # p = profile_form.save()
                # print("p---->",p)
                print("just user--->",user)
                print("user_form--->",user_form.data,request.FILES)
                # get the profile of the created user
                print("before calling profile--->")
                profile = Profile.objects.get(user=user)
                print("ppppppp----->",profile)
                # profile = Profile.objects.set(user=user)
                print("After calling profile--->")
                # get the uplloaded picture if any
                file = request.FILES.get("profile_pic")
                print("file--->",file)
                if(file != None):
                    # profile_pic = file
                    profile.profile_pic = file
                    # profile.profile_pic = file  # add the provided pic to that user profile
                profile.bio = request.POST["bio"]
                # profile.bio = request.POST["bio"]
                # profile.save()  # save the updates to user profile
                profile.save()
                log(profile.profile_pic.url)
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
            profile_form = ProfileForm()
        # context = {"user_form": user_form}
        context = {"user_form": user_form, "profile_form": profile_form}
        return render(request, 'user/register.html', context)
    else:
        return HttpResponseRedirect("/")


def login_view(request):
    """this custom login view does the following:
    1- checks if request comes from an already logged in user so it redirects him to hompage again
    2- check if the method is post and then the submitted form is valid
    3- check if the credentials are correct using authenticate method 
    4- check if user isn't registered takes him back to login back
    5- if user is registered but locked redirects him to blocked page"""

    if(not request.user.is_authenticated):  # check if user is already logged in
        if request.method == "POST":
            # using named parameter as request.Post isn't the first parameter by default
            login_form = LoginForm(data=request.POST)
            if(login_form.is_valid()):
                username = request.POST['username']
                password = request.POST["password"]
                # authenticate the user with provided data
                user = authenticate(username=username, password=password)
                if user is not None:  # user authenticated
                    if(isLocked(user)):
                        log(user.username + " blocked user")
                        # redirect the user to a custom page for blocked users
                        return HttpResponseRedirect("/user/blocked")
                    else:
                        login(request, user)
                        log(user.username + " logged in successfully")
                        # redirect to user homepage
                        return HttpResponseRedirect("/")
                else:
                    log("cannot login from login page")

            else:
                log("invalid login form")
        else:
            login_form = LoginForm()
        context = {"login_form": login_form}
        return render(request, 'user/login.html', context)
    else:
        return HttpResponseRedirect("/")


def profile(request):
    if(request.user.is_authenticated):
        user = request.user  # get the current user
        # get the profile related to that user
        userprofile = Profile.objects.get(user=user)
        context = {"user": user, "userprofile": userprofile}
        return render(request, "user/profile.html", context)
    else:
        return HttpResponseRedirect("/")





def blocked(request):
    # this view will be fired when a locked user tries to login
    if(not request.user.is_authenticated):
        admins = User.objects.all().filter(is_staff__exact=True)
        return render(request, "user/blocked.html", {"admins": admins})
    return HttpResponseRedirect("/")











# Create your views here.


def say_dashboard(request):
    return render(request, 'dashboard/base.html', {})


def say_blogs(request):
    all_categories = Categories.objects.all()
    # category = Categories.objects.get(id=cat_id)
    # cat_user = Categories.objects.from_queryset(users=request.user)
    user = request.user
    context = {'categories': all_categories,  'user': user}
    return render(request, 'user/blogs.html', context)




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

# # new post
# def new_post(request):
#     form = post_form()
#     # user_id = request.user.id
#     # print(user_id)
#     if request.method == 'POST':
#         form = post_form(request.POST, request.FILES)
#         post = form.save(commit=False)
#         print(form)
#         # post.user_id = int(user_id)
#         # print(form)
#         if form.is_valid():
#             post.save()
#             return HttpResponseRedirect(
#                 '#')

#     context = {'p_form': form}
#     return render(request, 'dashboard/newpost.html', context)

# add new tag 
def new_tag(request):
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/alltag/')
    else:
        context = {"pt_form": form}
        return render(request,"dashboard/newtag.html",context)


# delete
def delete_tag(request, tag_id):
    tag = Tags.objects.get(id=tag_id)
    tag.delete()
    return HttpResponseRedirect('/alltag/')



# get all tags
def getAllTag(request):
    all_tag= Tags.objects.all()
    context = {'tags': all_tag}
    return render(request, 'dashboard/alltag.html', context)

# edit tag
def edit_tag(request, tag_id):
    tag = Tags.objects.get(id=tag_id)
    form = TagForm(instance=tag)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/alltag/')

    context = {'pt_form': form}
    return render(request, 'dashboard/newtag.html', context)


# Categories





# def subscribe_category(request, c_id):
#     category = Categories.objects.get(pk=c_id)
#     # user = User.objects.get(pk = request.user.id)
#     # user = request.user
#     user = request.user
#     username = request.user.username
#     user_email = request.user.email
#     category_name = category.categoryName
#     send_mail('successfully subscribed','Thank you '+ username +'\nYou have successfully subscribed to ' + category_name + ' category' , 'noreply@iblog.com', [user_email])
#     category.users.add(user)

#     # return HttpResponseRedirect("/category_details/" + c_id)    #/category/all/  or /home/
#     return HttpResponseRedirect("/")


# def unsubscribe_category(request, c_id):
#     category = Categories.objects.get(pk=c_id)
#     # user = User.objects.get(pk = request.user.id)
#     # user = request.user
#     user = request.user
#     username = request.user.username
#     user_email = request.user.email
#     category_name = category.categoryName
#     send_mail('successfully unsubscribed','Thank you '+ username +'\nYou have successfully unsubscribed from ' + category_name + ' category' , 'noreply@iblog.com', [user_email])

#     category.users.remove(user)
#     return HttpResponseRedirect("/")

# def is_subscribed(request,u_id):
#     category = Categories.objects.get(fk=u_id)




def subscribe(request, cat_id):
    user = request.user
    category = Categories.objects.get(id=cat_id)
    category.user.add(user)
    # send email to user after subscription
    try:
        send_mail("subscribed to a new category", 'hello ,'+user.fname+" "+user.lname+'\nyou have just subscribed to category '+category.title,
                  'dproject.os40@gmail.com', [user.email], fail_silently=False,)
    except Exception as ex:
        log("couldn't send email message"+str(ex))
    return HttpResponseRedirect('/')


def unsubscribe(request, cat_id):
    user = request.user
    category = Categories.objects.get(id=cat_id)
    category.user.remove(user)
    return HttpResponseRedirect('/')

# add category
def new_post(request):
    form = post_form()
    if request.method == 'POST':
        form = post_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/allpost/')

    context = {'p_form': form}
    return render(request, 'dashboard/newpost.html', context)





# delete post
def post_delete(request, post_id):
    post = Posts.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/allpost/')

# get all posts
def getAllPost(request):
    all_post = Posts.objects.all()
    context = {'posts': all_post}
    return render(request, 'dashboard/post.html', context)

#edit post
def edit_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            picture = request.FILES.get('picture')
            if (picture):
                if(post.picture):
                    delete_profile_pic(post.picture)
                post.picture = picture
            post.user = request.user

            # tag_list = getTags(request.POST.get('tag'))
            post.save()
            # queryset = Tag.objects.filter(name__in=tag_list)
            # post.tags.set(queryset)
            return HttpResponseRedirect('/allpost')
    else:
        form = post_form(instance=post)
        context = {"p_form": form}
        return render(request, "dashboard/newpost.html", context)




#all user

def getAllUser(request):
    all_user =User.objects.all()
    context = {'all_user': all_user}
    return render(request, 'dashboard/alluser.html', context)