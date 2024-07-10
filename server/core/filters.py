import django_filters
from . models import Ads

class AdsFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='price')

    class Meta:
        model = Ads
        fields = []