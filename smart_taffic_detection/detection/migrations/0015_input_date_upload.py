# Generated by Django 4.1.7 on 2023-03-13 17:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0014_remove_input_weather_choice_input_intersection_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='date_upload',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
