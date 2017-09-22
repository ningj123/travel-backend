from django.contrib import admin

from .models import SchoolBusTimeSchedules, SchoolBusWeekSchedules, SchoolBus, SchoolBusReserve


@admin.register(SchoolBusTimeSchedules)
class SchoolBusSchedulesAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(SchoolBusWeekSchedules)
class SchoolBusWeekSchedulesAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(SchoolBus)
class SchoolBusAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('schedule', 'date')


@admin.register(SchoolBusReserve)
class SchoolBusReserveAdmin(admin.ModelAdmin):
    save_on_top = True
