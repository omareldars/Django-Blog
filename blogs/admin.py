from django.contrib import admin
from .models import Categories, Tags, Posts, Replies, Comments, ForbiddenWords
from .models import Profile
from django.contrib.auth.models import User

# Register your models here.


# admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Tags)
admin.site.register(Posts)
admin.site.register(Replies)
admin.site.register(Comments)
admin.site.register(ForbiddenWords)


class UserProfileAdmin(admin.ModelAdmin):
    list_display =['user','is_locked','undesired_words_count']
admin.site.register(Profile,UserProfileAdmin)
