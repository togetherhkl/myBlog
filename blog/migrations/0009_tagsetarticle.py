# Generated by Django 3.2.15 on 2022-09-22 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_articles'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagSetArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.articles', verbose_name='博文名')),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.tag', verbose_name='标签名')),
            ],
        ),
    ]
