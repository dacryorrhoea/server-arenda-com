# from django.shortcuts import render
from rest_framework import generics, permissions, mixins, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User

from . serializer import RegisterSerializer, UserSerializer, LogoutSerializer, ProfileSerializer
from . permissions import IsOwnerOnly


class Register(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })

# нууууууууу кое как работает
class Logout(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsOwnerOnly,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Ok')


class AccountInfo(generics.GenericAPIView):
    permission_classes = (IsOwnerOnly, permissions.IsAuthenticated)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class ProfileInfo(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
