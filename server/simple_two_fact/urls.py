from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ConfirmCodeCreate.as_view()),
    path('approve/', ConfirmCodeApprove.as_view())
]