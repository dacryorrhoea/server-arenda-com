from rest_framework import generics, exceptions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
import requests
import random

from .models import *


class ConfirmCodeCreate(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            phone_number = request.data['phone_number']
        except:
            return Response('Не указан номер телефона.')

        confirm_code = 0
        while(confirm_code <= 99999):
            confirm_code = confirm_code * 10 + random.randint(0, 9)

        code = ConfirmCode.objects.create(code=confirm_code)

        requests.get(
            f'https://api.telegram.org/bot2043706009:AAGyOD6rkIbtv93jtWFBeEgCAoBoXYlP98I/sendMessage',
            params={
                'chat_id': '699063672',
                'text': f'Человек с номером {phone_number}! Воть ваш код подтверждения: {confirm_code}'
            }
        )
        return Response({
            "id": str(code.id)
        })

class ConfirmCodeApprove(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            saved_code = ConfirmCode.objects.get(id=request.data['confirm_code_id'])
        except Exception as e:
            return HttpResponseBadRequest('He указан id кода подтверждения')
        
        if saved_code.code != int(request.data['confirm_code']):
            return HttpResponseBadRequest('Неверный код подтверждения')
        else:
            saved_code.delete()
            return Response('Ok')

