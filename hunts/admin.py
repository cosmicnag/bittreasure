from django.contrib import admin
from models import *

class LocationInline(admin.StackedInline):
    model = Location


class TreasureHuntAdmin(admin.ModelAdmin):
    inlines = [LocationInline]


admin.site.register(TreasureHunt, TreasureHuntAdmin) 
# Register your models here.
