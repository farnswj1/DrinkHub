from django_filters import FilterSet, CharFilter
from .models import Drink, Ingredient
from django.db.models import CharField

class DrinkFilter(FilterSet):
    class Meta:
        model = Drink
        fields = ["Name", "Type", "Alcohol"]
        filter_overrides = {
            CharField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }


class IngredientFilter(FilterSet):
    class Meta:
        model = Ingredient
        fields = ["Name", "Alcohol"]
        filter_overrides = {
            CharField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }