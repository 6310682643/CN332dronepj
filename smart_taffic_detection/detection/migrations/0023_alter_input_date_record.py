# Generated by Django 4.1.7 on 2023-03-13 18:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0022_alter_input_date_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='date_record',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='date'),
        ),
    ]
