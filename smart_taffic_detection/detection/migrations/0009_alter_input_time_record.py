# Generated by Django 4.1.7 on 2023-03-10 16:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0008_alter_input_time_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='time_record',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='time'),
        ),
    ]
