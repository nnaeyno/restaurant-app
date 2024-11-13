from django_filters import rest_framework as filters
from meal.models import Dish

class DishFilter(filters.FilterSet):
    sub_category = filters.NumberFilter(field_name='sub_category__id')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    available = filters.BooleanFilter(field_name='is_available')
    has_allergens = filters.BooleanFilter(method='filter_allergens')

    class Meta:
        model = Dish
        fields = ['sub_category', 'name', 'available']

    def filter_allergens(self, queryset, name, value):
        if value is True:
            return queryset.filter(ingredients__is_allergen=True).distinct()
        elif value is False:
            return queryset.exclude(ingredients__is_allergen=True)
        return queryset