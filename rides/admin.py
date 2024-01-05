from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Region, Location, CustomUser


# Register your models here.
# @admin.register(Profile)
# class Profile(admin.ModelAdmin):
#     pass

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name',
        'gender', 'DOB', 'DL_date'
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'gender')
        }),
        ('Hitch Driver Info', {
            'fields': ('DOB', 'DL_date', 'adr_street', 'adr_city', 'adr_zip', 'adr_country', 'phone', 'contactable')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
        
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),        
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'gender')
        }),
        ('Hitch Driver Info', {
            'fields': ('DOB', 'DL_date', 'adr_street', 'adr_city', 'adr_zip', 'adr_country', 'phone', 'contactable')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
        
    )

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Region)

admin.site.register(Location)