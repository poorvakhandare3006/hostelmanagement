# Generated by Django 2.2.11 on 2021-08-26 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enroll', models.CharField(max_length=10, null=True, unique=True)),
                ('hostel', models.CharField(max_length=10, null=True)),
                ('course', models.CharField(max_length=20, null=True)),
                ('roll', models.CharField(max_length=20, null=True, unique=True)),
                ('room', models.CharField(max_length=20, null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('address', models.CharField(max_length=3000, null=True)),
                ('contact', models.CharField(max_length=9999999999, null=True)),
                ('p_contact', models.CharField(max_length=9999999999, null=True)),
                ('image', models.ImageField(default='', upload_to='student/images')),
                ('student', models.BooleanField(default=False)),
                ('so', models.BooleanField(default=False)),
                ('academics', models.BooleanField(default=False)),
                ('guard', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('out_time', models.DateTimeField(null=True)),
                ('in_time', models.DateTimeField(null=True)),
                ('out_reason', models.BooleanField(default=False)),
                ('out', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]