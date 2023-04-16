# Generated by Django 4.1.7 on 2023-04-03 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_rule_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rule_user_status',
            field=models.CharField(choices=[(0, 'Admin'), (1, 'Moderator'), (3, 'User')], default=3, max_length=3, verbose_name='Роль пользователя'),
        ),
        migrations.DeleteModel(
            name='RuleUser',
        ),
    ]
