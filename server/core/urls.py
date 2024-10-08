from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'ads', AdViewSet, basename='ads_for_all')
router.register(r'user/manage/ads', AdViewSetForLessor, basename='ads_for_lessor')
router.register(r'user/manage/rezervations', ReservationViewSetForRentor, basename='reservations_for_rentor')
router.register(r'unreg/user/create/rezervations', ReservationViewSetForUnregUser, basename='reservations_for_unreg_user')
router.register(r'user/manage/payment', PaymentViewSet, basename='reservation_payment')
router.register(r'user/manage/review', ReviewViewSetForRentor, basename='review_for_rentor')
router.register(r'user/manage/favorite', FavoriteViewSetForRentor, basename='favorite_for_rentor')

router.register(r'addresses', AddressesViewSet, basename='all_addresses')
# router.register(r'user/manage/history', BrowsingHistoryViewSetForRentor, basename='history_for_rentor')

urlpatterns = router.urls