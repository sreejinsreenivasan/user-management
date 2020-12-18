from django.shortcuts import render
from rest_framework import generics
from .serializers import (
    UserSerializer,
    UpdateUserSerializer,
    UserProfileSerailizer,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.models import Client, Country, Store, User, UserProfile

# Create your views here.


class UserDetailView(generics.RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        elif self.request.method == "PATCH":
            return UpdateUserSerializer


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerailizer
    queryset = UserProfile.objects.all()
