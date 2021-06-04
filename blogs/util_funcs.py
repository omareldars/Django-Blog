from .models import Profile
from blog_project.settings import BASE_DIR
import os
from blogs.logger import log


# def promote_to_staff(user):
#     user.is_staff = True
#     user.save()


# def promote_to_super_user(user):
#     promote_to_staff(user)
#     user.is_superuser = True
#     user.save()


def lock_user(user):
    profile = Profile.objects.get(user=user)
    profile.is_locked = True
    profile.save()


def unlock_user(user):
    profile = Profile.objects.get(user=user)
    profile.is_locked = False
    profile.save()


def isLocked(user):
    return user.profile.is_locked


def demote_user(user):
    user.is_staff = False
    user.save()


def delete_profile_pic(profile_pic):
    try:
        pic_url = BASE_DIR+profile_pic.url
        if(pic_url.endswith("defaultImage.png")):
            pass
        else:
            os.remove(pic_url)
            log("deleted profile pic ")
    except Exception as ex:
        log("no pic"+str(ex))
