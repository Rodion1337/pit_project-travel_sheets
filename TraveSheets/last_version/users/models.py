from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    RuleUser=(
        ('0', 'Admin'),
        ('1', 'Moderator'),
        ('3', 'User'),
    )
    icon_user = models.ImageField(verbose_name = 'Иконка пользователя', upload_to = 'icon_user', height_field=None, width_field=None, max_length=None, blank=True, null=True, default='icon_user/default-user-profile-picture.jpg',)
    rule_user_status = models.CharField(verbose_name='Роль пользователя', choices=RuleUser, default='3', max_length=3)