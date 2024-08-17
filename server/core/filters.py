import django_filters
from . models import Ad

class AdFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='price')
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')
    type_flats = django_filters.CharFilter(field_name='type_flats', lookup_expr='icontains')

    wifi = django_filters.BooleanFilter(field_name='wifi')
    towel = django_filters.BooleanFilter(field_name='towel')
    bed_linen = django_filters.BooleanFilter(field_name='bed_linen')
    tv = django_filters.BooleanFilter(field_name='tv')
    drier = django_filters.BooleanFilter(field_name='drier')
    microwave = django_filters.BooleanFilter(field_name='microwave')
    electric_kettle = django_filters.BooleanFilter(field_name='electric_kettle')
    balcony = django_filters.BooleanFilter(field_name='balcony')
    street = django_filters.CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = Ad
        fields = []