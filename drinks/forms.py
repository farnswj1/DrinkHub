from django.forms import ModelForm
from .models import Recipe

class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["Drink", "Quantity", "Measurement"]


class RecipeUpdateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["Drink", "Quantity", "Measurement"]



