# Generated by Django 3.2.15 on 2022-09-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_category_jumpaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='jumpaddress',
            field=models.CharField(default='#', max_length=128),
        ),
    ]
