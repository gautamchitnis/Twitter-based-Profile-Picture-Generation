from django.db import models
from django.contrib.auth.models import User


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'group_{0}/{1}'.format(instance.group.id, filename)


class Group(models.Model):
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)


class PFP(models.Model):
    pfp = models.ImageField(upload_to=user_directory_path)
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)


class GroupMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class GroupTags(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    tags = models.CharField(max_length=10000)


class MemberTags(models.Model):
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    tags = models.CharField(max_length=10000)
