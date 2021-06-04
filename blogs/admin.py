from django.contrib import admin
from .models import Categories, Tags, Posts, Comments, ForbiddenWords
from .models import Profile
from django.contrib.auth.models import User

# Register your models here.
class CustomPost(admin.ModelAdmin):
    fieldsets = (['write post', {'fields': ['title', 'content', 'picture', 'author', 'tag']}],
                 ['likes', {'fields': ['likes']}], ['dislikes', {'fields': ['dislikes']}])
    list_display = ['title', 'content', 'picture', 'created_at']
    list_filter = ['created_at', 'title']


# admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Tags)
admin.site.register(Posts, CustomPost)
admin.site.register(Comments)
admin.site.register(ForbiddenWords)


class UserProfileAdmin(admin.ModelAdmin):
    list_display =['user', 'is_locked', 'undesired_words_count']
admin.site.register(Profile,UserProfileAdmin)
