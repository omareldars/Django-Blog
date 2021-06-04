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
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="user/logout.html"), name='logout'),
    path("profile/", views.profile, name="profile"),
    path('blocked/', views.blocked, name="blocked"),
    path('newword/', views.add_forbiden_word, name='add-word'),
    path('deleteword/<word_id>', views.delete_forbiden_word, name='delete-word'),
    path('editword/<word_id>', views.edit_forbiden_word, name='edit-word'),
    path('allforbidden/', views.getAllWord, name='all-word'),
    path('forbidden_words/', views.getAllWord, name='all-word'),
    path('newpost/', views.new_post, name="add-post"),
    path('deletepost/<post_id>', views.post_delete, name='delete-post'),
    path('post/edit/<post_id>', views.edit_post, name='edit-post'),
    path('allpost/', views.getAllPost, name='all-post'),
    path('newtag/', views.new_tag, name='add-tag'),
    path('alltag/', views.getAllTag, name='all-tags'),
    path('edittag/<tag_id>', views.edit_tag, name='edit-tag'),
    path('deletetag/<tag_id>', views.delete_tag, name='delete-tag'),
    path('subscribe/<cat_id>', views.subscribe),
    path('unsubscribe/<cat_id>', views.unsubscribe),
    path('deleteuser/<user_id>', views.user_delete, name='delete-user'),
    path('alluser/', views.getAllUser, name="all-user"),
]
