# Generated by Django 2.2.11 on 2021-08-30 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20210830_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='image',
        ),
    ]
