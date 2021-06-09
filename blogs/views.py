import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import post_form, category_form, ForbiddenWordForm,TagForm, RegistrationForm,LoginForm,ProfileForm, EditProfileForm, ChangePasswordForm, Comments_Form
from .logger import log
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from .util_funcs import isLocked
import os
from .models import Categories, Tags, Posts, Comments, ForbiddenWords, Profile
from .util_funcs import delete_profile_pic
from .util_funcs import *
from django.core.paginator import Paginator
from django.db.models import Q






# about us page
def about(request):
    return render(request, 'user/about.html')



# register
def register(request):
    """this custom login view does the following:
    1- checks if request comes from an already logged in user so it redirects him to hompage again
    2- check if the method is post and then the submitted form is valid"""
    if(not request.user.is_authenticated):
        if request.method == "POST":
            user_form = RegistrationForm(request.POST)
            # get the form and the upladed files
            profile_form = ProfileForm(request.POST, request.FILES)
            if user_form.is_valid():
                user = user_form.save()  # save the user into database and return it
                # get the profile of the created user
                profile = Profile.objects.get(user=user)
                # get the uplloaded picture if any
                file = request.FILES.get("profile_pic")
                if(file != None):
                    profile.profile_pic = file
                profile.bio = request.POST["bio"]
                profile.save()
                log(profile.profile_pic.url)
                log("created a new user successfully with username: " + user.username)  # for debugging purposes
                user = authenticate(username=request.POST["username"], password=request.POST["password1"])
                if user is not None:
                    login(request, user)
                    try:
                        EmailMessage('Welcome to  I-Blog', 'The Team: \n 1- Omar \n 2- Ahmed \n 3- Eslam \n 4- Ekhlas \n 5- Asmaa \n welcome you','english.iti41@gmail.com', [user.email]).send(fail_silently=False)
                    except Exception as ex:
                        log("couldn't send email message"+str(ex))
                    # redirect to user profile page
                    return HttpResponseRedirect("/profile")
                else:
                    log("cannot login from registration form")
            else:
                log("invalid registration form")  # for debugging purposes
        else:
            user_form = RegistrationForm()
            profile_form = ProfileForm()
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
                        return HttpResponseRedirect("/blocked")
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
    if(is_authorized_admin(request)):
       return render(request, 'dashboard/base.html', {})
    return HttpResponseRedirect("/")


def posts(request):
    posts = Posts.objects.all()
    popular_posts = Posts.objects.order_by('-likes')[:5]
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Categories.objects.all()
    tags = Tags.objects.all()[:10]
    user = request.user

    context = {'page_obj': page_obj, 'categories': categotries,
               'tags': tags, 'user': user, 'popular_posts': popular_posts, 'posts':posts}
    return render(request, 'user/blogs.html', context)



def say_blogs(request):
    all_categories = Categories.objects.all()
    # category = Categories.objects.get(id=cat_id)
    # cat_user = Categories.objects.from_queryset(users=request.user)
    posts=Posts.objects.all()
    user = request.user
    context = {'categories': all_categories,  'user': user, 'post':posts}
    return render(request, 'user/blogs.html', context)



# view blog-details and create comment or reply on purpose
def blog_detail(request, id):
    post = Posts.objects.get(id=id)
    categories = Categories.objects.all()
    tags = Tags.objects.all()
    user = request.user
    forbidden = ForbiddenWords.objects.all()
    comments = Comments.objects.filter(post=post).order_by('-id')
    if request.method == 'POST':
        comment_form = Comments_Form(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            for word in forbidden:
                if str(word) in content:
                    user.profile.undesired_words_count +=1
                    user.profile.save()
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comments.objects.get(id=reply_id)
            Comments.objects.create(post=post, user=user, content=content, reply=comment_qs)
            comment_form = Comments_Form()
    else:
        comment_form = Comments_Form()
    context = {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
            "categories": categories,
            "tags": tags,
            "user": user
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

# add forbiden word


def add_forbiden_word(request):
    form = ForbiddenWordForm()
    if request.method == 'POST':
        form = ForbiddenWordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/allforbidden/')
    else:
        context = {"pt_form": form}
        return render(request, "dashboard/newforbiden.html", context)

# delete forbidden word


def delete_forbiden_word(request, word_id):
    title = ForbiddenWords.objects.get(id=word_id)
    title.delete()
    return HttpResponseRedirect('/allforbidden/')

# get all forbiden word


def getAllWord(request):
    all_word = ForbiddenWords.objects.all()
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

# take comment text to be replaced with the original comment on post


# def check_forbidden_words_in_comment(request, content):
#     content_arr = content.split(",")
#     all_forbidden_words = ForbiddenWords.objects.all()
#     for word in all_forbidden_words:
#         replaced = ""
#         if content.find(word.title):
#             for c in word.title:
#                 replaced += "*"
#             content = content.replace(word.title, replaced)

#     return HttpResponseRedirect('/forbidden_words/')


# def check_profanity(content):
#     filtered = ''
#     first_word = True
#     for word in content.split():
#         if not first_word:
#             filtered += ' '
#         first_word = False
#         if ForbiddenWords.objects.filter(title=word.lower()):
#             filtered += ('*' * len(word))
#         else:
#             filtered += word
#     return filtered

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
        return render(request, "dashboard/newtag.html", context)


# delete
def delete_tag(request, tag_id):
    tag = Tags.objects.get(id=tag_id)
    tag.delete()
    return HttpResponseRedirect('/alltag/')


# get all tags
def getAllTag(request):
    all_tag = Tags.objects.all()
    context = {'tags': all_tag}
    return render(request, 'dashboard/alltag.html', context)


# get tag list
def getTags(string):
    tag_list = list(string.split(" "))
    for tag in tag_list:
        if not Tags.objects.filter(title=tag):
            Tags.objects.create(title=tag)
    return tag_list



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
        form = post_form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.picture = request.FILES.get('picture')
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            tags_query = Tags.objects.filter(title__in=tag_list)
            post.tag.set(tags_query)
            return HttpResponseRedirect('/allpost/')
            # form.save()
            # post.save()
            # print("Photo---->", request.FILES, "\n \n \n")
            # print("post---->", post, "\n \n \n")
            # print("form-1--->", form, "\n \n \n")
            # print("form-2--->", form, "\n \n \n")
    else:
        context = {'p_form': form}
        return render(request, 'dashboard/newpost.html', context)

def user_new_post(request):
    form = post_form()
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.picture = request.FILES.get('picture')
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            tags_query = Tags.objects.filter(title__in=tag_list)
            post.tag.set(tags_query)
            return HttpResponseRedirect('/')
            # form.save()
            # post.save()
            # print("Photo---->", request.FILES, "\n \n \n")
            # print("post---->", post, "\n \n \n")
            # print("form-1--->", form, "\n \n \n")
            # print("form-2--->", form, "\n \n \n")
    else:
        context = {'p_form': form}
        return render(request, 'user/newpost.html', context)



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

# delete post
def post_delete(request, post_id):
    post = Posts.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/allpost/')

def user_post_delete(request, post_id):
    post = Posts.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('')


# get all posts
def getAllPost(request):
    all_post = Posts.objects.all()
    context = {'posts': all_post}
    return render(request, 'dashboard/post.html', context)


# edit post
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
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            tag_query = Tags.objects.filter(title__in=tag_list)
            post.tag.set(tag_query)
            return HttpResponseRedirect('/allpost/')
    else:
        form = post_form(instance=post)
        context = {"p_form": form}
        return render(request, "dashboard/newpost.html", context)



def user_edit_post(request, post_id):
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
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            tag_query = Tags.objects.filter(title__in=tag_list)
            post.tag.set(tag_query)
            return HttpResponseRedirect('/')
    else:
        form = post_form(instance=post)
        context = {"p_form": form}
        return render(request, "user/newpost.html", context)





# all user

def getAllUser(request):
    all_user = User.objects.all()
    context = {'all_user': all_user}
    return render(request, 'dashboard/alluser.html', context)


# like post
def like_post(request, id):
    post = get_object_or_404(Posts, pk=id)
    post_likes = post.likes.all()
    post_disliked = post.dislikes.all()
    user = request.user
    if (user not in post_likes):
        if(user not in post_disliked):
            post.likes.add(user)
            post.save()
    else:
        post.likes.remove(user)
        post.save()
    return HttpResponseRedirect("/post/"+id)



# post dislikes and auto delete after 10 dislikes
def dislike_post(request, id):
    post = get_object_or_404(Posts, pk=id)
    print(post)
    post_likes = post.likes.all()
    post_disliked = post.dislikes.all()
    user = request.user
    if (user not in post_disliked):
        if(user not in post_likes):
            post.dislikes.add(user)
            post.save()
    else:
        post.dislikes.remove(user)
        post.save()
    total = post.total_dislikes()
    if(total == 10):
        post.delete()
        return HttpResponse("<h1> this post has been deleted </h1>")
    return HttpResponseRedirect("/post/"+id)


# edit comment
def commentEdit(request, id):
    comment = Comments.objects.get(id=id)
    if request.method == 'POST':
        form = Comments_Form(request.POST, instance=comment.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('deletecomment')
    else:
        form = Comments_Form(instance=comment)
    return render(request, 'post_detail.html', {'form': form})

# delete comment
def commentDelete(request, post_id, com_id):
    comment = Comments.objects.get(id=com_id)
    comment.delete()
    return HttpResponseRedirect('/post/'+post_id)




    

def edit_profile(request):
    """this edit profile view does the following:
    1- checks that user is logged in already or redirects him to homepage
    2- check if the method is post and then the submitted forms are valid
    3- update user info and save
    4- if success redirects the user to profile page"""

    if(request.user.is_authenticated):
        if request.method == "POST":
            edit_form = EditProfileForm(data=request.POST)
            profile_form = ProfileForm(request.POST, request.FILES)
            user = request.user
            if(edit_form.is_valid()):
                log("valid edit form")
                file = request.FILES.get("profile_pic")
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.profile.bio = request.POST["bio"]
                if(file != None):
                    if(user.profile.profile_pic != None):
                        delete_profile_pic(user.profile.profile_pic)
                    user.profile.profile_pic = file
                user.save()
                user.profile.save()
                log(user.username + "  updated his profile")
                return HttpResponseRedirect("/profile")
            else:
                log("invalid change form")
                return HttpResponseRedirect("/")
        else:
            user = request.user
            user_data = {"first_name": user.first_name,
                         "last_name": user.last_name}
            bio_data = {"bio": user.profile.bio}
            edit_form = EditProfileForm(data=user_data)
            profile_form = ProfileForm(data=bio_data)
            context = {"edit_form": edit_form, "profile_form": profile_form}
            return render(request, "user/edit.html", context)


# delete user
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return HttpResponseRedirect('/alluser/')


def promote_to_staff(user):
    """this function can be used to promot a normal user to be a staff user with the required permissions"""
    user.is_staff = True
    user.save()


def promote_to_super_user(user):
    promote_to_staff(user)
    user.is_superuser = True
    user.save()


def is_authorized_admin(request):
    if(request.user.is_authenticated):
        if(request.user.is_staff):
            return True
    return False


def manager_promote_user(request, id):
    """promote a specific user to become an admin with all determined permissions
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        promote_to_staff(user)
        log(request.user.username+" promoted " + user.username+".")
        return HttpResponseRedirect("/alluser/")
    else:
        return HttpResponseRedirect("/")


def change_password(request):
    """this change password view does the following:
    1- checks that user is logged in already or redirects him to homepage
    2- check if the method is post and then the submitted forms are valid
    3- update user password and save
    4- if success redirects the user to profile page"""

    if(request.user.is_authenticated):
        if request.method == 'POST':
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                log("changed password for "+user.username)
                return HttpResponseRedirect('/profile')
            else:
                log("couldn't change password for "+user.username)
        else:
            form = ChangePasswordForm(request.user)
        return render(request, 'user/change_password.html', {
            'form': form
        })
    else:
        return HttpResponseRedirect("/")



def promote(request, id):
    return manager_promote_user(request, id)


def super_promote_admin(request, id):
    """promote a specific admin to become a super user with the highest permissions
    @params : request  , id"""

    current_user = request.user
    if(is_authorized_admin(request)):
        if(current_user.is_superuser):
            user = User.objects.get(pk=id)
            promote_to_super_user(user)
            log(current_user.username+" promoted " +
                user.username+" to a super user.")
        return HttpResponseRedirect("/alluser/")
    else:
        return HttpResponseRedirect("/")


def promote_admin_to_super(request, id):
    return super_promote_admin(request, id)

#lock user
def lock_user(user):
    profile = Profile.objects.get(user=user)
    profile.is_locked = True
    profile.save()

#unlock user
def unlock_user(user):
    profile = Profile.objects.get(user=user)
    profile.is_locked = False
    profile.save()



def admin_lock_user(request, id):
    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        lock_user(user)
        log(request.user.username+" locked " + user.username+".")
        return HttpResponseRedirect("/alluser")
    else:
        return HttpResponseRedirect("/")

def admin_unlock_user(request, id):
    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        unlock_user(user)
        log(request.user.username+" unlocked " + user.username+".")
        return HttpResponseRedirect("/alluser")
    else:
        return HttpResponseRedirect("/")

def lock(request, id):
    return admin_lock_user(request, id)

def unlock(request, id):
    return admin_unlock_user(request, id)


def search(request):
    query = request.GET.get('q')
    print(query," -----> ",type(query))
    posts = Posts.objects.filter(Q(title__contains=query))
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Categories.objects.all()
    tags = Tags.objects.filter(Q(title__contains=query))[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'user/blogs.html', context)


def about(request):
    return render(request, 'user/about.html')



def tagPosts(request, tag_id):
    tag = Tags.objects.get(id=tag_id)
    # posts = tag.post_set.all()
    posts = Posts.objects.filter(tag=tag)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Categories.objects.all()
    tags = Tags.objects.all()[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'user/blogs.html', context)


def categoryPosts(request, cat_id):
    category = Categories.objects.get(id=cat_id)
    posts = Posts.objects.filter(category=category)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Categories.objects.all()
    tags = Tags.objects.all()[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'user/blogs.html', context)
