# Generated by Django 3.2.15 on 2022-09-22 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ftag',
            old_name='ftag_CreateDate',
            new_name='ftag_createdate',
        ),
    ]
