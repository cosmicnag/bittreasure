from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
import datetime
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException, PermissionDenied,\
    ParseError, MethodNotAllowed, AuthenticationFailed
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from serializers import UserSerializer, TreasureHuntSerializer, UserTreasureHuntSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.gis import geos
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

@api_view(['POST'])
@csrf_exempt
def participate(request,pk):
    usertreasurehunt = UserTreasureHunt()
    usertreasurehunt.user = request.user
    treasurehunt = get_object_or_404(TreasureHunt,pk=pk)
    usertreasurehunt.treasurehunt = treasurehunt 
    if treasurehunt.entryfee == 0:
        usertreasurehunt.paid = True
    usertreasurehunt.save()
    return Response({'address':usertreasurehunt.address})

@api_view(['GET'])
def logout(request):
    auth_logout(request)
    return Response({'detail': 'User logged out'})

@api_view(['GET'])
def clues(request,pk):
    treasurehunt = get_object_or_404(TreasureHunt,pk=pk)
    user = request.user
    if not treasurehunt.issequential:
        locations = Location.objects.filter(treasurehunt=treasurehunt)
    else:
        # TODO handle ordering properly
        userlocations = UserLocation.objects.filter(location__treasurehunt=treasurehunt).filter(user=user).order_by('-location__order')
        if userlocations.count() > 0:
            currentlocation = userlocations[-1].location
            #if currentlocation.confirmed: #TODO
            location = Location.objects.filter(treasurehunt=treasurehunt).filter(order__gt=currentlocation.order)[0]
        else:
            location = Location.objects.filter(treasurehunt=treasurehunt).order_by('order')[0]
        locations = [location]
    return Response({
        'clues': [l.get_clue() for l in locations]
    })


@api_view(['POST'])
def gotit(request,pk):
    lat = request.POST.get('lat', None)
    lon = request.POST.get('lon', None)
    payload = request.POST.get('payload', None)
    user = request.user
    if not lat or not lon:
        raise APIException("fuck off, i need lat and lon")
    location = get_object_or_404(Location, pk=pk)
    point = geos.Point(float(lat), float(lon))
    distance = point.distance(location.point) * 1000
    treasurehunt = location.treasurehunt

    if UserTreasureHunt.objects.filter(treasurehunt=treasurehunt, user=user, paid=True).count() == 0:
        raise APIException("you are not part of this treasure hunt. pay up or go away.")

    if (location.radius < distance):
        raise APIException("you are not close enough")
    else:
        userlocation = UserLocation()
        userlocation.user = user
        userlocation.location = location
        if treasurehunt.isphysical and payload:
            if payload == location.payload:
                userlocation.isconfirmed = True
        if not treasurehunt.isphysical:
            userlocation.isconfirmed = True
        userlocation.save()
        ret = {
            'text': location.text
        }
        if not treasurehunt.isphysical:
            ret['payload'] = location.payload
        return Response(ret)

#TODO: remove
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

class UserTreasureHunts(generics.ListAPIView):
    serializer_class = UserTreasureHuntSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return UserTreasureHunt.objects.filter(user=user)
