import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=100)



class Tags(models.Model):
    title = models.CharField(max_length=100)



class ForbiddenWords(models.Model):
    title = models.CharField(max_length=100)


class Users(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    username = models.CharField(max_length=70)
    email = models.EmailField()
    age = models.IntegerField(default=18, validators=[MaxValueValidator(60), MinValueValidator(18)])
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)




class Replies(models.Model):
    content = models.TextField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()




class Comments(models.Model):
    content = models.TextField()
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    reply_id = models.ForeignKey(Replies, on_delete=models.CASCADE)



class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    picture = models.FilePathField(path="blogs/statics/images")
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)






