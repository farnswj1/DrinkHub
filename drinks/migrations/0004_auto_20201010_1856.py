# Generated by Django 3.1 on 2020-10-10 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0003_auto_20201009_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='Measurement',
            field=models.CharField(max_length=15),
        ),
    ]
