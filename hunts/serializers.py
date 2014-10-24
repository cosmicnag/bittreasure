from rest_framework import serializers
from models import User, TreasureHunt
from django.contrib.auth import login, authenticate, logout
from rest_framework.exceptions import PermissionDenied


class UserSerializer(serializers.ModelSerializer):

    token = serializers.Field(source='get_token')

    def restore_object(self, attrs, instance=None):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        request = self.context['request']

        #create new user
        if not instance:
            user = User.objects.create_user(email, password)
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            login(request, user)
            return user
        else:
            if request.user.id != instance.id \
                    and not request.user.is_superuser:
                raise PermissionDenied()
            if password and password != '':
                instance.set_password(password)
            instance.save()
            return instance

    def save_object(self, *args, **kwargs):
        pass

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token',)
        write_only_fields = ('password',)


class TreasureHuntSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreasureHunt
        fields = ('id', 'name', 'description', 'place', 'issequential', 'isphysical', 'starttime',)
