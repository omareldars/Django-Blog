from django.contrib import admin
from .models import Users, Categories, Tags, Posts, Replies, Comments, ForbiddenWords
# Register your models here.


admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(Tags)
admin.site.register(Posts)
admin.site.register(Replies)
admin.site.register(Comments)
admin.site.register(ForbiddenWords)