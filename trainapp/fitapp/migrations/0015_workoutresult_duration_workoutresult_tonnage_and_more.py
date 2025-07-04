# Generated by Django 5.2.1 on 2025-06-22 23:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0014_alter_workout_date_alter_workoutresult_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutresult',
            name='duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='workoutresult',
            name='tonnage',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2025, 6, 23, 1, 43, 27, 741936)),
        ),
        migrations.AlterField(
            model_name='workoutresult',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 6, 23, 1, 43, 27, 743426)),
        ),
    ]
