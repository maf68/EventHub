# Generated by Django 4.2 on 2023-04-17 19:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0004_alter_event_request"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="Request",
            new_name="request_status",
        ),
    ]
