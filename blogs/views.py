from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
# Create your views here.
def say_blogs(request):
    return render(request, 'admin/index.html',{})