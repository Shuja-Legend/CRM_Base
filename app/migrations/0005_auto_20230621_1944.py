# Generated by Django 3.2.18 on 2023-06-21 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_lead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='following',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profession',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]
