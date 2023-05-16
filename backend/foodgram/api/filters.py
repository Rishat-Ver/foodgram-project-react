from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']
