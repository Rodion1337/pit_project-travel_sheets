# Generated by Django 4.1.7 on 2023-04-02 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_icon_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon_user',
            field=models.ImageField(blank=True, default='icon_user/default-user-profile-picture.jpg', null=True, upload_to='icon_user', verbose_name='Иконка пользователя'),
        ),
    ]
