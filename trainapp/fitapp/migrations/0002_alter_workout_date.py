# Generated by Django 5.1.6 on 2025-04-19 20:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(default=datetime.datetime(2025, 4, 19, 22, 43, 30, 413617)),
        ),
    ]
