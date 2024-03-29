# Generated by Django 3.2.15 on 2022-11-02 19:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_auto_20221101_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='article_createdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 2, 19, 39, 51, 384667), verbose_name='发表日期'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_createdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 2, 19, 39, 51, 383998), verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_img',
            field=models.FileField(default='media/user_avatar/default_avatar.png', max_length=128, upload_to='user_avatar/', verbose_name='用户头像'),
        ),
    ]
