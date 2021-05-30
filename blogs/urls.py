from django.urls import path, include
from blogs import views

urlpatterns = [
    path('', views.say_blogs, name='blogs'),
]