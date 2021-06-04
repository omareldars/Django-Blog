import datetime
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

fs = FileSystemStorage()

# class Users(models.Model):
#     fname = models.CharField(max_length=50)
#     lname = models.CharField(max_length=50)
#     username = models.CharField(max_length=70)
#     email = models.EmailField()
#     age = models.IntegerField(default=18, validators=[MaxValueValidator(60), MinValueValidator(18)])
#     is_blocked = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)

#     def __str__(self):
#         return self.fname + ' ' + self.lname

# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(User, null=True, blank=True, related_name='categories')

    def __str__ (self):
        return self.title
    class Meta:
        verbose_name_plural = "Categories"
        

class Tags(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class ForbiddenWords(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title




class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="dislikes", blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to="./static/image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_at = datetime.datetime.now()
    # updated_at = datetime.datetime.now()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tags, blank=True)
    # category = models.ManyToManyField(Categories, related_name='posts')
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def conclusion(self):
        return self.content[:50] + "..."

    def __str__(self):
        return self.title

    @property
    def picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url

    class Meta:
        ordering = ('-created_at',)


class Comments(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comments', null=True, related_name="replies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return '{} commented on {}.'.format(str(self.user.username), self.post.title)

    def filter_comment(self):
        forbidden = ForbiddenWords.objects.all()
        for word in forbidden:
            self.content = self.content.replace(str(word), '*' * len(str(word)))
        return self.content



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        verbose_name="profile picture", storage=fs, default='defaultImage.png')
    # the cumulative number of undesiredwords the user has used
    undesired_words_count = models.IntegerField(default=0)
    # determine whether the user is locked or not
    is_locked = models.BooleanField(default=False)
    bio = models.TextField(max_length=200, default="")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
