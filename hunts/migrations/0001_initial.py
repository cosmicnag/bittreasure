# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('mobileno', models.CharField(max_length=32, blank=True)),
                ('firstname', models.CharField(max_length=64, blank=True)),
                ('lastname', models.CharField(max_length=64, blank=True)),
                ('changed', models.DateTimeField(null=True, editable=False)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('isactive', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('radius', models.IntegerField(default=10, help_text=b'in metres')),
                ('text', models.TextField()),
                ('clue', models.TextField(blank=True)),
                ('payload', models.TextField(blank=True)),
                ('extra', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreasureHunt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('place', models.CharField(max_length=255)),
                ('starttime', models.DateTimeField(null=True, blank=True)),
                ('issequential', models.BooleanField(default=False)),
                ('isphysical', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(related_name='ownhunts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('isconfirmed', models.BooleanField(default=False)),
                ('location', models.ForeignKey(to='hunts.Location')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserTreasureHunt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('treasurehunt', models.ForeignKey(to='hunts.TreasureHunt')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='treasurehunt',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='hunts.UserTreasureHunt'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='treasurehunt',
            field=models.ForeignKey(blank=True, to='hunts.TreasureHunt', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='hunts.UserLocation'),
            preserve_default=True,
        ),
    ]
