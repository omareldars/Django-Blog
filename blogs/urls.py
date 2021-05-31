from django.urls import path, include
from blogs import views

urlpatterns = [
    path('', views.say_blogs, name='blogs'),
    path('post', views.say_post, name='post'),
    path('post/<id>',views.blog_detail, name='post_details'),
]