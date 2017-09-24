from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Driver, UcenterReserveWrapper

class CustomizeUserAdmin(UserAdmin):
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('truename', 'avatar', 'usertype')}),
        ('权限控制', {'fields': ('can_apply', 'is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')})
    )


class DriverAdmin(admin.ModelAdmin):
    save_on_top = True


class UcenterReserveWrapperAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'user',
        'reserve_pk',
        'reserve_type',
        'reserve_status'
    )

admin.site.register(User, CustomizeUserAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(UcenterReserveWrapper, UcenterReserveWrapperAdmin)