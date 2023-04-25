from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.contrib.auth.models import User
from UserInfo.models import UserDopInfo
from django.db import models


@receiver(post_save, sender=User)
def create_dop_info(sender, instance, created, **kwargs):
    print(created,sender.username)
    if created:
        print(f'create user: {instance.username}')
        UserDopInfo.objects.create(user=instance.id)
        UserDopInfo.objects.save()