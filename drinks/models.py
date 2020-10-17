from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

DRINK_TYPES = [
    ("Beer", "Beer"),
    ("Cocktail", "Cocktail"),
    ("Cocoa", "Cocoa"),
    ("Coffee/Tea", "Coffee/Tea"),
    ("Homemade Liqueur", "Homemade Liqueur"),
    ("Milk/Float/Shake", "Milk/Float/Shake"),
    ("Ordinary Drink", "Ordinary Drink"),
    ("Other/Unknown", "Other/Unknown"),
    ("Punch/Party Drink", "Punch/Party Drink"),
    ("Shot", "Shot"),
    ("Soft Drink/Soda", "Soft Drink/Soda")
]

# Create your models here.
class Drink(models.Model):
    Name = models.CharField(
        unique = True, 
        null = False, 
        max_length = 30,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9 /#'-\.]+$",
                message="Name must be alphanumeric and may contain only: ./#'-."
            )
        ]
        )
    Type = models.CharField(
        null = False, 
        max_length = 20, 
        choices=DRINK_TYPES,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z /]+$",
                message="Name must be alphanumeric and may also contain dashes."
            )
        ]
    )
    Alcohol = models.BooleanField(null = False, default = False)
    Datestamp = models.DateField(null = False, default=timezone.now)

    class Meta:
        ordering = ['Name']
    
    def get_absolute_url(self):
        return reverse("drink-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.Name}'


class Ingredient(models.Model):
    Name = models.CharField(
        unique = True, 
        null = False, 
        max_length = 30,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9 /#'-\.]+$",
                message="Name must be alphanumeric and may contain only: ./#'-."
            )
        ]
    )
    Alcohol = models.BooleanField(null = False, default = False)

    class Meta:
        ordering = ['Name']
    
    def get_absolute_url(self):
        return reverse("ingredient-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.Name}'


class Recipe(models.Model):
    Drink = models.ForeignKey(Drink, null = False, on_delete = models.CASCADE)
    Ingredient = models.ForeignKey(Ingredient, null = False, on_delete = models.CASCADE)
    Quantity = models.DecimalField(
        max_digits = 4, 
        decimal_places = 2, 
        null = False, 
        validators=[MinValueValidator(0.01)]
    )
    Measurement = models.CharField(
        null = False, 
        max_length = 15,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z -\.]+$",
                message="""Measurement must be alphanumeric and may 
                           contain only spaces, periods and dashes."""
            )
        ]
    )
 
    class Meta:
        unique_together = (("Drink", "Ingredient"),)

    def get_absolute_url(self):
        return reverse("drink-detail", kwargs={"pk": self.Drink.pk})
    
    def __str__(self):
        return f"{self.Drink.Name}: {self.Quantity} {self.Measurement} {self.Ingredient.Name}"
