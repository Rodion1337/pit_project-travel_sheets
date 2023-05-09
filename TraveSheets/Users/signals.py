from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from Users.models import Profile


@receiver(post_save, sender=User)
def create_dop_info(sender, instance, created, **kwargs):
    if created:
        print(f'create user: {instance.username}')
        Profile.objects.create(user=instance)

