# Generated by Django 4.1.7 on 2023-04-10 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_event_attendees_event_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image_urls',
        ),
    ]
