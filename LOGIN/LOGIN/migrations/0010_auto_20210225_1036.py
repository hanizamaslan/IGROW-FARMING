# Generated by Django 3.1.2 on 2021-02-25 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LOGIN', '0009_workshop_programmename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='Member',
        ),
        migrations.RemoveField(
            model_name='discussion',
            name='ProfilePictures',
        ),
    ]
