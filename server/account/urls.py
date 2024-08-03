from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'profile', ProfileInfo, basename='profile_info')
# router.register(r'user/profile', UserProfileInfo, basename='curr_user_profile_info')

urlpatterns = [
      path('', include(router.urls)),
      path('register/', Register.as_view()),
      path('logout/', Logout.as_view()),
      path('user/profile/', AccountInfo.as_view()),
]
