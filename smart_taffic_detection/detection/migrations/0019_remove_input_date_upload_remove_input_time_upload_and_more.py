# Generated by Django 4.1.7 on 2023-03-13 17:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0018_alter_input_date_record_alter_input_time_record'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='date_upload',
        ),
        migrations.RemoveField(
            model_name='input',
            name='time_upload',
        ),
        migrations.AlterField(
            model_name='input',
            name='date_record',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='input',
            name='time_record',
            field=models.TimeField(default=django.utils.timezone.now, null=True, verbose_name='time'),
        ),
    ]
