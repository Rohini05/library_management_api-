# Generated by Django 3.2.8 on 2021-10-22 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0006_library_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='library',
            name='password',
        ),
    ]
