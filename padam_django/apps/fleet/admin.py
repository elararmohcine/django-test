from django.contrib import admin

from . import models
from .models import BusShift

@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'start_time', 'end_time')
    
