import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import post_form, category_form
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
