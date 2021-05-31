from django.urls import path, include
from blogs import views

urlpatterns = [
    path('dashboard/', views.say_admin, name='admin'),
    path('', views.say_blogs, name='blogs'),
    path('post', views.say_post, name='post'),
    path('new/', views.new_category),
    path('all/', views.getAllCategory),
    path('edit/<category_id>', views.edit_category),
    path('delete/<category_id>', views.delete_category),
]