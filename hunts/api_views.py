from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
import datetime
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException, PermissionDenied,\
    ParseError, MethodNotAllowed, AuthenticationFailed
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from serializers import UserSerializer, TreasureHuntSerializer
from django.views.decorators.csrf import csrf_exempt
from models import *


class UsersView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    paginate_by = 50

    def create(self, *args, **kwargs):
        #FIXME: move validation into serializer validate methods
        email = self.request.POST.get('email', None)

        if User.objects.filter(email=email).count() > 0:
            raise APIException("duplicate email")

        password = self.request.POST.get('password', '')
        if password == '':
            raise ParseError("No password supplied")

        return super(UsersView, self).create(*args, **kwargs)

    def get_queryset(self):
        return User.objects.all()


@api_view(['GET'])
def logout(request):
    auth_logout(request)
    return Response({'success': 'User logged out'})


@api_view(['POST'])
@csrf_exempt
def login(request):
    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    user = authenticate(username=email, password=password)
    if user is not None:
        auth_login(request, user)
        user_data = {
            'token': Token.objects.get(user=user).key,
        }
        return Response(user_data)
    raise AuthenticationFailed("Username / password do not match")


class TreasureHuntsView(generics.ListCreateAPIView):
    serializer_class = TreasureHuntSerializer   
 
    def get_queryset(self, *args, **kwargs):
        return TreasureHunt.objects.all()

