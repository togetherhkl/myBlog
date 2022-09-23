# Generated by Django 3.2.15 on 2022-09-22 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_tagsetarticle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(verbose_name='评论内容')),
                ('comment_like', models.BigIntegerField(verbose_name='点赞数')),
                ('comment_createdate', models.DateTimeField(verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.articles', verbose_name='评论的文章')),
                ('comment_fid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.comments', verbose_name='父评论')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.users', verbose_name='评论者')),
            ],
        ),
    ]
