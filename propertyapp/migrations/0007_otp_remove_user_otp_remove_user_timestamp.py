# Generated by Django 4.2 on 2023-04-23 11:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propertyapp', '0006_alter_user_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('otp', models.CharField(default='1234', max_length=4)),
                ('timestamp', models.DateField(default=datetime.datetime(2023, 4, 23, 11, 7, 27, 788682))),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='timestamp',
        ),
    ]
