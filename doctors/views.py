from django.shortcuts import render , redirect ,HttpResponse 
from django.http import JsonResponse
from .models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from django.contrib.auth.hashers import make_password , check_password
import jwt


class CreateUserProfile(APIView) :
    def post(self, request):
        data = request.data.copy()
        data['set_password'] = make_password(data['set_password'])
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = Mentaluser.objects.get(id = serializer.data['id'])
            refresh = Myrefreshtoken.for_user(user)
            access_token  = str(refresh.access_token)
            refresh_token = str(refresh)
            response = Response(
                {
                    "data" : serializer.data,
                    "user_id" : serializer.data['id'],
                }
            )
            response.set_cookie("access_token", value=access_token, httponly=True, secure=True,max_age=60*60*24*7 ,  samesite='None')
            response.set_cookie("refresh_token", value=refresh_token, httponly=True, secure=True, max_age=60*60*24*7,  samesite='None')
            print("Cookies set:", response.cookies)
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

class AutoLogin(APIView) :
    def get(self , request) :
        try :
            refresh_token = request.COOKIES.get("refresh_token")

            if refresh_token is None :
                return Response({
                    "message" : "Invalid token"
                } , status= status.HTTP_401_UNAUTHORIZED)

            new_token = Myrefreshtoken(refresh_token)

            new_access_token = str(new_token.access_token)
            new_refresh_token = str(new_token)
            

            response = Response(
                {
                    "message" : "Token Renewed"
                },
                status=status.HTTP_201_CREATED
            )

            response.set_cookie("access_token", value=new_access_token, httponly=True, secure=True, max_age=60*60 ,  samesite='None')
            response.set_cookie("refresh_token", value=new_refresh_token, httponly=True, secure=True, max_age=60*60*24*7,  samesite='None')
            print("Cookies set:", response.cookies)
            return response
        except Exception as e :
            print("The Error is :" , str(e))
            return Response({
                "message" : "we can find the token sorry sign up again"
            },
            status=status.HTTP_400_BAD_REQUEST)

        


    

class Authstatus(APIView) :
    def get(self , request) :
        token = request.COOKIES.get("access_token")  # Get JWT from HTTP-only cookie
        print("token is:", token)

        if not token:
            return Response({"authenticated": False, "error": "Token not found"}, status=401)

        try:
            print("start decoding")
            payload = jwt.decode(token,  options={"verify_signature": False}, algorithms=["HS256"])
            print("Decoded Payload:", payload)  # Debugging
            return Response({"authenticated": True, "user_id": payload["user_id"]})
        
        except jwt.ExpiredSignatureError:
            return Response({"authenticated": False, "error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"authenticated": False, "error": "Invalid token"}, status=401)
        except Exception as e:
            return Response({"authenticated": False, "error": "Server error"}, status=500)