# products/filters.py
import django_filters
from django.db.models import Q
from products.models import Product, ProductVariant

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(method='filter_category')  # Updated to use custom method for filtering by multiple slugs
    color = django_filters.CharFilter(method='filter_color')
    size = django_filters.CharFilter(field_name="variants__size__size", lookup_expr='icontains')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'color', 'size', 'in_stock']
        
    def filter_category(self, queryset, name, value):
        # Split the category slugs by comma to filter by multiple categories
        slugs = value.split(',')
        return queryset.filter(category__slug__in=slugs).distinct()
    
    def filter_color(self, queryset, name, value):
        if value:
            if ProductVariant.objects.filter(color=value).exists():
                return queryset.filter(variants__color=value).distinct()
            else:
                return queryset.none()
        return queryset

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(variants__quantity__gt=0).distinct()
        return queryset.filter(variants__quantity__lte=0).distinct()
