# Generated by Django 3.1 on 2020-10-10 01:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0002_recipe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drink',
            options={'ordering': ['Name']},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['Name']},
        ),
        migrations.AddField(
            model_name='ingredient',
            name='Alcohol',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='drink',
            name='Type',
            field=models.CharField(choices=[('Beer', 'Beer'), ('Cocktail', 'Cocktail'), ('Cocoa', 'Cocoa'), ('Coffee/Tea', 'Coffee/Tea'), ('Homemade Liqueur', 'Homemade Liqueur'), ('Milk/Float/Shake', 'Milk/Float/Shake'), ('Ordinary Drink', 'Ordinary Drink'), ('Other/Unknown', 'Other/Unknown'), ('Punch/Party Drink', 'Punch/Party Drink'), ('Shot', 'Shot'), ('Soft Drink/Soda', 'Soft Drink/Soda')], max_length=20),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='Quantity',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]