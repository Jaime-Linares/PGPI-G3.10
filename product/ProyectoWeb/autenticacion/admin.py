from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_group', 'is_staff', 'is_active')

    def get_group(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_group.short_description = 'Rol'  

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
