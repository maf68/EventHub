# Generated by Django 4.2 on 2023-04-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0003_event_request"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="Request",
            field=models.CharField(
                choices=[
                    ("Accept", "Accept"),
                    ("Reject", "Reject"),
                    ("Pending", "Pending"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
    ]
