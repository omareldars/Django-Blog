import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=100)

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


class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(Users, related_name="likes")
    dislikes = models.ManyToManyField(Users, related_name="dislikes")
    picture = models.ImageField()
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.content


class Comments(models.Model):
    content = models.TextField()
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name="comments", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content


class Replies(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, related_name="replies", on_delete=models.CASCADE, null=True)
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()

    def __str__(self):
        return self.content
