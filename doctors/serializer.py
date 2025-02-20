from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Mentaluser
        fields = '__all__'


class Myrefreshtoken(RefreshToken) :
    @classmethod
    def for_user(self , user) :
        token = super().for_user(user)
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        return token