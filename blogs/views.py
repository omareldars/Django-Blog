import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import post_form, category_form,ForbiddenWordForm
from .models import Users, Categories, Tags, Posts, Replies, Comments, ForbiddenWords

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
