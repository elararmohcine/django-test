from django.contrib import admin

from . import models
from .models import BusShift, BusStop

@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'start_time', 'end_time')

@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('place', 'bus_shift', 'stop_order')
    ordering = ['bus_shift', 'stop_order']
    
