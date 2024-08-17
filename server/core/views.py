from rest_framework import generics, mixins, viewsets, exceptions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework import filters
import datetime
import requests
import random
from transliterate import translit

from simple_two_fact.models import ConfirmCode
from .models import *
from .serializers import *
from .permissions import *
from .filters import *
from .pagination import *


class AddressesViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = Ad.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]


# список и изъятие, с фильтрацией и пагинацией для объявлений
class AdViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [AllowAny]

    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AdFilter
    ordering_fields = ['price']
    # search_fields = ['address'] , filters.SearchFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return AdPartialSerializer
        return super().get_serializer_class()

class PaymentViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = PaymentReceipt.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        try:
            sum = self.request.data['sum']
            card_name = self.request.data['card_name']
            card_holder = self.request.data['card_holder']
            card_cvv = self.request.data['card_cvv']
            # payment_code = self.request.data['payment_code']
            given_reservation = Reservation.objects.get(id=self.request.data['reservation_id'])
        except:
            raise exceptions.ValidationError('Некорректные данные запроса')
        
        # тут должен быть запрос к сервису оплаты и прочее но будет принт
        print(f'Чек на сумму {sum} - {card_name} - {card_holder} - {card_cvv}')

        # 'если оплата проходит'
        given_reservation.approve_status = True
        given_reservation.save(update_fields=['approve_status'])
        
        serializer.save(reservation=given_reservation)


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


# бронирование для незарег пользователей
class ReservationViewSetForUnregUser(mixins.CreateModelMixin,
                                     viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):        
        # дальше почти аналогично созданию брони для зарег юзера
        try:
            given_ad = Ad.objects.get(id=self.request.data['ad_id'])
        except:
            raise exceptions.ValidationError('He указан id объявления или такого объявления не существует')

        
        if self.request.data['end_lease'] < self.request.data['begin_lease']:
            raise exceptions.ValidationError('Heверная последовательность')

        for elem in Reservation.objects.all().filter(ad=given_ad).values_list('begin_lease', 'end_lease'):
            if not (datetime.datetime.strptime(self.request.data['end_lease'], '%Y-%m-%d').date() <= elem[0] or 
                    datetime.datetime.strptime(self.request.data['begin_lease'], '%Y-%m-%d').date() >= elem[1]):
                raise exceptions.ValidationError('Уже забронировано на эти даты')
        
        # скрытое создание профиля пользователя
        try:
            username = translit(
                f'{str.lower(self.request.data['first_name'])}_{str.lower(self.request.data['last_name'])}',
                language_code='ru', reversed=True
            )
            password = username + str(random.randint(1111, 9999))

            # если пользователь имеется в базе то ничего создавать не надо
            if User.objects.filter(username=username):
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    password = password,
                    first_name=self.request.data['first_name'],
                    last_name=self.request.data['last_name'],
                )
                user.groups.add(2)
        except:
            raise exceptions.ValidationError('Некорректные персональные данные')

        serializer.save(owner=user, ad=given_ad)

        requests.get(
            f'https://api.telegram.org/bot2043706009:AAGyOD6rkIbtv93jtWFBeEgCAoBoXYlP98I/sendMessage',
            params={
                'chat_id': '699063672',
                'text': f'Вы (ваш логин: {username} и ваш пароль: {password}) забронировали жильё на сайте arenda.com на даты с {self.request.data['begin_lease']} по {self.request.data['end_lease']}'
            }
        )

# бронирование для зарегистрированых пользователей
class ReservationViewSetForRentor(mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    permission_classes = [IsRentorOnly]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        # получение объявления
        try:
            given_ad = Ad.objects.get(id=self.request.data['ad_id'])
        except:
            raise exceptions.ValidationError('He указан id объявления или такого объявления не существует')

        # дополнительная проверка на доступность да, хотя аналогичная логика есть и на клиенте
        if self.request.data['end_lease'] < self.request.data['begin_lease']:
            raise exceptions.ValidationError('He верная последовательность')

        for elem in Reservation.objects.all().filter(ad=given_ad).values_list('begin_lease', 'end_lease'):
            if not (datetime.datetime.strptime(self.request.data['end_lease'], '%Y-%m-%d').date() <= elem[0] or 
                    datetime.datetime.strptime(self.request.data['begin_lease'], '%Y-%m-%d').date() >= elem[1]):
                raise exceptions.ValidationError('Уже забронировано на эти даты')
        
        # сохранение
        serializer.save(owner=self.request.user, ad=given_ad)

        # отправка оповещения о брони
        requests.get(
            f'https://api.telegram.org/bot2043706009:AAGyOD6rkIbtv93jtWFBeEgCAoBoXYlP98I/sendMessage',
            params={
                'chat_id': '699063672',
                'text': f'Вы {self.request.user} забронировали жильё на сайте arenda.com на даты с {self.request.data['begin_lease']} по {self.request.data['end_lease']}'
            }
        )


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
