from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    icon_user = models.ImageField(verbose_name = 'Icon user', upload_to = 'icon_user', height_field=None, width_field=None, max_length=None, blank=True, null=True)