from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from blogs.models import Posts,Categories
from blogs.forms import post_form,category_form
# Create your views here.

def say_blogs(request):
    return render(request, 'user/blogs.html', {})
    

def say_admin(request):
    return render(request, 'admin/base.html',{})
  

def say_post(request):
    return render(request, 'user/post-details.html',{})


# add category
def new_category(request):
    form = category_form()
    if request.method == 'POST':
        form =  category_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/all')

    context = {'ct_form': form}
    return render(request, 'admin/newcategory.html', context)
    
# edit category
def edit_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    form = category_form(instance=category)
    if request.method == 'POST':
        form = category_form(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/all')

    context = {'ct_form': form}
    return render(request, 'admin/newcategory.html', context)


# delete
def delete_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    category.delete()
    return HttpResponseRedirect('/admin/all')

#get all category
def getAllCategory(request):
    all_category = Categories.objects.all()
    context = {'categories':all_category }
    return render(request, 'admin/category.html', context)
    