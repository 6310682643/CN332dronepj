# Generated by Django 4.1.7 on 2023-03-13 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0015_input_date_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='time_upload',
            field=models.TimeField(default=datetime.time),
        ),
    ]
