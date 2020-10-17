from django.contrib import admin
from .models import Drink, Ingredient, Recipe

# Register your models here.
admin.site.register(Drink)
admin.site.register(Ingredient)
admin.site.register(Recipe)