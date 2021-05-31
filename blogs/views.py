import requests
from django.shortcuts import render
from .models import Users, Categories, Tags, Posts, Replies, Comments, ForbiddenWords

# Create your views here.
def say_blogs(request):
    return render(request, 'user/blogs.html', {})

def say_post(request):
    return render(request, 'user/post-details.html',{})

def blog_detail(request, id):
    post = Posts.objects.get(id = id)
    comments = Comments.objects.filter(post=post)
    context = {
        "post":post,
        "comments": comments,
    }
    return render(request, 'user/post-details.html', context)