import django_filters
from . models import Ad

class AdFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='price')
    address = django_filters.CharFilter(field_name='address')

    class Meta:
        model = Ad
        fields = []