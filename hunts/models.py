from django.contrib.gis.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,\
    PermissionsMixin
import datetime
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=UserManager.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    #Better field type to use?
    mobileno = models.CharField(max_length=32, blank=True)
    firstname = models.CharField(max_length=64, blank=True)
    lastname = models.CharField(max_length=64, blank=True)
    #type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    changed = models.DateTimeField(null=True, editable=False)
    created = models.DateTimeField(null=True, editable=False)
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    objects = UserManager()
    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.is_superuser

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        self.changed = datetime.datetime.today()
        if self.created is None:
            self.created = self.changed
        return super(User, self).save(*args, **kwargs)

    def get_short_name(self):
        return self.email

    def get_token(self):
        return Token.objects.get(user=self).key

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class TreasureHunt(models.Model):
    admin = models.ForeignKey(User, related_name='ownhunts')
    name = models.CharField(max_length=255)
    description = models.TextField()
    place = models.CharField(max_length=255)
    entryfee = models.IntegerField(default=0)
    starttime = models.DateTimeField(blank=True, null=True)
    issequential = models.BooleanField(default=False)
    isphysical = models.BooleanField(default=False)
    users = models.ManyToManyField('User', through='UserTreasureHunt')
    def __unicode__(self):
    	return self.name

class Location(models.Model):
    treasurehunt = models.ForeignKey('TreasureHunt', blank=True, null=True)
    order = models.IntegerField(default=0)
    point = models.PointField()
    radius = models.IntegerField(default=10, help_text="in metres")
    text = models.TextField()
    clue = models.TextField(blank=True)
    payload = models.TextField(blank=True)
    extra = models.TextField(blank=True)
    users = models.ManyToManyField('User', through='UserLocation')

    def get_clue(self):
        return {
            'locationid': self.id,
            'clue': self.clue
        }

class UserLocation(models.Model):
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    timestamp = models.DateTimeField()
    isconfirmed = models.BooleanField(default=False)

class UserTreasureHunt(models.Model):
    user = models.ForeignKey(User)
    treasurehunt = models.ForeignKey(TreasureHunt)
    address = models.CharField(max_length=255,blank=True)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.datetime.now()
            self.address = '192L6LuTkU9gJtN7DQg8i93Fxzk3GTPEUZ'
        return super(UserTreasureHunt, self).save(*args, **kwargs)
