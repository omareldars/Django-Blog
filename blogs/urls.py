from django.urls import path, include
from blogs import views

urlpatterns = [
    path('admin/', views.say_blogs),
]