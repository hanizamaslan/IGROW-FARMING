# Generated by Django 3.1.2 on 2021-04-01 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LOGIN', '0014_workshop'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='Description',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='workshop',
            name='NoOfEvent',
            field=models.CharField(default='', max_length=150),
        ),
    ]
