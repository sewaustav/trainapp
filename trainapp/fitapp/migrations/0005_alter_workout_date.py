# Generated by Django 5.1 on 2025-04-20 01:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0004_workout_name_alter_workout_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(default=datetime.datetime(2025, 4, 20, 3, 34, 49, 864644)),
        ),
    ]
