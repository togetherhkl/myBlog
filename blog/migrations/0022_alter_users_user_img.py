# Generated by Django 3.2.15 on 2022-10-11 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_articles_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_img',
            field=models.FileField(blank=True, max_length=128, null=True, upload_to='usersimg/', verbose_name='用户头像'),
        ),
    ]