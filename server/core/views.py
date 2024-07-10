from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from .models import Ads
from .serializers import AdsDetailSerializer, AdsListSerializer
from .filters import AdsFilter


class AdsView(ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsDetailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdsFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return AdsListSerializer
        return super().get_serializer_class()
    
