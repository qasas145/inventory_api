from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializer import CustomUserSerializer, LoginSerializer, CreateUserSerializer
from .authentication import generate_access_token, generate_refresh_token
from .models import CustomUser


# Create your views here.



class UserView(viewsets.ModelViewSet) :
    http_method_names = ['get',]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer




class LoginView(APIView) :


    serializer_class = LoginSerializer

    def post(self, *args, **kwargs) :

        serializer = self.serializer_class(data = self.request.data)

        if not serializer.is_valid() :
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        user_authenticated = authenticate(
            username = serializer.validated_data['email'],
            password = serializer.validated_data['password']
        )
        if user_authenticated :
            data = {
                "access" : generate_access_token({'user_id' : user_authenticated.id}),
                "refresh" : generate_refresh_token(),
            }
            return Response(data, status = status.HTTP_200_OK)
        return Response("Please enter the correct data", status = status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView) :

    serializer_class = CreateUserSerializer

    def post(self, *args, **kwargs) :
        serializer = self.serializer_class(data = self.request.data)

        if not serializer.is_valid() :
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)
        

