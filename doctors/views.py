from django.shortcuts import render , redirect ,HttpResponse 
from django.http import JsonResponse
from .models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from django.contrib.auth.hashers import make_password , check_password


class CreateUserProfile(APIView) :
    def post(self, request):
        data = request.data.copy()
        data['set_password'] = make_password(data['set_password'])
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = Mentaluser.objects.filter(email = data['email']).first()
            refresh = Myrefreshtoken.for_user(user)
            access_token  = str(refresh.access_token)
            refresh_token = str(refresh)
            response = Response(
                {
                    "data" : serializer.data,
                    "user_id" : user.id,
                    "access_token" : access_token,
                    "refresh_token" : refresh_token
                }
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Loginuser(APIView) :
    def post(self , request) :
        user = request.data
        email = user.get('email')
        password = user.get('set_password')
        authuser = Mentaluser.objects.filter(email = email).first()
        if authuser is None  :
            return Response({
                "message" : "The username Doesnt exist",

            } , status = status.HTTP_404_NOT_FOUND)
        if authuser and check_password(password , authuser.set_password):
            response = Response(
                {
                "message": f"Hello {authuser.username}, login successful!",
                },
                status = status.HTTP_201_CREATED
            )
                # response.set_cookie(
                #     'access_token', value=access_token, httponly=True, secure=True, samesite='Strict'
                # )
                # response.set_cookie(
                #     'refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict'
                # )
            return response
        else :
            return Response({"message"  : "Password mismatched"} , status=status.HTTP_404_NOT_FOUND)