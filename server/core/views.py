from rest_framework import generics, mixins, viewsets, exceptions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
import datetime

from .models import *
from .serializers import *
from .permissions import *
from .filters import *
from .pagination import *


# список и изъятие, с фильтрацией и пагинацией для объявлений
class AdViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [AllowAny]

    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return AdPartialSerializer
        return super().get_serializer_class()


# создание и прочее для объявление, из проверок пока только базовая валидация
class AdViewSetForLessor(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Ad.objects.all()
    permission_classes = [IsLessorOnly]
    serializer_class = AdDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def filter_queryset(self, queryset):
        queryset = queryset.filter(owner=self.request.user)
        return super().filter_queryset(queryset)


# бронирование с проверкой свободны ли выбранные даты
class ReservationViewSetForRentor(mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    permission_classes = [IsRentorOnly]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        if 'ad_id' in self.request.data:
            given_ad = Ad.objects.get(id=self.request.data['ad_id'])
        else:
            raise exceptions.ValidationError('He указан id объявления')
        
        if self.request.data['end_lease'] < self.request.data['begin_lease']:
            raise exceptions.ValidationError('He верная последовательность')

        for elem in Reservation.objects.all().filter(ad=given_ad).values_list('begin_lease', 'end_lease'):
            if not (datetime.datetime.strptime(self.request.data['end_lease'], '%Y-%m-%d').date() <= elem[0] or 
                    datetime.datetime.strptime(self.request.data['begin_lease'], '%Y-%m-%d').date() >= elem[1]):
                raise exceptions.ValidationError('Уже забронировано на эти даты')
        
        serializer.save(owner=self.request.user, ad=given_ad)


# создание и прочее для коментариев с дополнительной проверкой на завершение бронирования
class ReviewViewSetForRentor(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = [IsRentorOnly]
    queryset = Review.objects.all()
    serializer_class = PublicViewReviewSerializer

    def perform_create(self, serializer):
        # if 
        serializer.save(owner=self.request.user)


# добавление/удаление избранного, из проверок: наличие в избранном у пользователя
class FavoriteViewSetForRentor(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsRentorOnly]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        if 'ad_id' in self.request.data:
            given_ad = Ad.objects.get(id=self.request.data['ad_id'])
        else:
            raise exceptions.ValidationError('He указан id объявления')
        
        if Favorite.objects.all().filter(owner=self.request.user).filter(ad=given_ad).exists():
            raise exceptions.ValidationError('Уже добавлено в избранное.')

        serializer.save(owner=self.request.user, ad=given_ad)


class BrowsingHistoryViewSetForRentor(mixins.CreateModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):
    permission_classes = [IsRentorOnly]
    queryset = BrowsingHistory.objects.all()
    serializer_class = BrowsingHistorySerializer

    def perform_create(self, serializer):
        if 'ad_id' in self.request.data:
            given_ad = Ad.objects.get(id=self.request.data['ad_id'])
        else:
            raise exceptions.ValidationError('He указан id объявления')
        
        if Favorite.objects.all().filter(owner=self.request.user).filter(ad=given_ad).exists():
            raise exceptions.ValidationError('Уже добавлено в историю просмотра')

        serializer.save(owner=self.request.user, ad=given_ad)
