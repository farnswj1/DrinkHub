# Generated by Django 3.1 on 2020-10-11 00:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0004_auto_20201010_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='Datestamp',
            field=models.DateField(default=datetime.date(2020, 10, 10)),
        ),
    ]
