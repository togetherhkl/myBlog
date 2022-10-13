# Generated by Django 3.2.15 on 2022-10-07 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_articles_article_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.tag', verbose_name='标签'),
        ),
    ]
