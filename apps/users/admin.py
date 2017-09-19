from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Driver

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

admin.site.register(User, CustomizeUserAdmin)
admin.site.register(Driver, DriverAdmin)