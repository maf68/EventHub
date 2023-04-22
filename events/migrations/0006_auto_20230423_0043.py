# Generated by Django 3.2.18 on 2023-04-22 21:43

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='request_status',
            field=models.CharField(choices=[('Accept', 'Accept'), ('Reject', 'Reject'), ('Pending', 'Pending')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[django.core.validators.MinValueValidator(datetime.date(2023, 4, 22))]),
        ),
    ]
