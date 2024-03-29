# Generated by Django 3.2.15 on 2022-10-13 10:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_alter_users_user_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_createdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 10, 8, 5, 976817), verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_img',
            field=models.FileField(default='media/user_avatar/default_avatar.png', max_length=128, upload_to='usersimg/', verbose_name='用户头像'),
        ),
    ]
