import datetime
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from blog_project.settings import MEDIA_ROOT,MEDIA_URL
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

class Users(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    username = models.CharField(max_length=70)
    email = models.EmailField()
    age = models.IntegerField(default=18, validators=[MaxValueValidator(60), MinValueValidator(18)])
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.fname + ' ' + self.lname

# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=100)
    # users = models.ManyToManyField(Users, null=True, blank=True)

    def __str__(self):
        return self.title
  

class Tags(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ForbiddenWords(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title




class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(Users, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(Users, related_name="dislikes",blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to=os.path.join(BASE_DIR, 'static/images'))
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now_add=True)
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    author = models.ForeignKey(Users, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tags, on_delete=models.PROTECT)
    # category = models.ManyToManyField(Categories, related_name='posts')
    category =models.ForeignKey(Categories,on_delete=models.PROTECT)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.content + '  likes: ' + str(self.total_likes()) + '  dislikes: ' + str(self.total_dislikes())


class Comments(models.Model):
    content = models.TextField()
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    post = models.ForeignKey(Posts, related_name="comments", on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.content


class Replies(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comments, related_name="replies", on_delete=models.PROTECT, null=True)
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()

    def __str__(self):
        return self.content
