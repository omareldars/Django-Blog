import requests
from django.shortcuts import render

# Create your views here.
def say_blogs(request):
    return render(request, 'user/blogs.html', {})