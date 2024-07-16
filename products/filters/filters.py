# products/filters.py
import django_filters
from products.models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category")
    color = django_filters.CharFilter(field_name="variants__color")
    size = django_filters.CharFilter(field_name="variants__size")
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'color', 'size','in_stock']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(variants__quantity__gt=0).distinct()
        return queryset.filter(variants__quantity__lte=0).distinct()
