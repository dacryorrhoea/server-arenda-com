from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Ads
from .serializers import AdsDetailSerializer, AdsListSerializer
from .filters import AdsFilter

class AdsView(ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdsFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return AdsListSerializer
        return super().get_serializer_class()
    
