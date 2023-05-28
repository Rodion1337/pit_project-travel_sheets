from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    RuleUser = (
        ('0', 'Admin'),
        ('1', 'Moderator'),
        ('3', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon_user = models.ImageField(verbose_name='Иконка пользователя',
                                  upload_to='icon_user', height_field=None,
                                  width_field=None, max_length=None,
                                  blank=True, null=True,
                                  default='icon_user/default-user-icon.jpg',)
    last_approve = models.DateField(verbose_name='Дата последней пройденной проверки',
                                    default='2022-12-31', auto_now=False,
                                    auto_now_add=False)

    def __str__(self) -> str:
        return 'доп. информация на ' + self.user.username
