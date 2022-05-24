from django.db import models


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class PFP(models.Model):
    pfp = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
