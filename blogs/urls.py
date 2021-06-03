from django.urls import path, include
from blogs import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.say_blogs, name='home'),
    path('dashboard/', views.say_dashboard, name='dashboard'),
    path('post/<id>', views.blog_detail, name='post_details'),
    path('new/', views.new_category, name='add-category'),
    path('all/', views.getAllCategory, name='all-categories'),
    path('edit/<category_id>', views.edit_category, name='edit-category'),
    path('delete/<category_id>', views.delete_category, name='delete-category'),
    path('register/',views.register , name='register'),
    path('login/',views.login_view , name='login'), 
    path("profile/",views.profile , name="profile"),
    path('blocked/',views.blocked,name="blocked"),
    path('newword/', views.add_forbiden_word, name='add-word'),
    path('deleteword/<word_id>', views.delete_forbiden_word, name='delete-word'),
    path('editword/<word_id>', views.edit_forbiden_word, name='edit-word'),
    path('allforbidden/', views.getAllWord, name='all-word'),
    path('forbidden_words/', views.getAllWord, name='all-word'),
    path('newpost/', views.new_post, name="add-post")
]
