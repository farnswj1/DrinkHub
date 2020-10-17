from django_filters import FilterSet, CharFilter
from .models import User
from django.db.models import CharField


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = ["username", "is_active", "is_superuser"]
        filter_overrides = {
            CharField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
