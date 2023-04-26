# Generated by Django 4.2 on 2023-04-26 02:10

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_announcement_image_alter_event_poster_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[django.core.validators.MinValueValidator(datetime.date(2023, 4, 26))]),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]