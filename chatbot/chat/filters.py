import django_filters
from .models import FAQ

class FAQFilter(django_filters.FilterSet):
    # Filter by category (exact match)
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')
    
    class Meta:
        model = FAQ
        fields = ['category']