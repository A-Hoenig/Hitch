from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Region, Location, CustomUser, Purpose, Vehicle, Driver_rating, Trip, Hitch_Request, Message

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name',
        'gender', 'DOB', 'DL_date'
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'user_image')
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

admin.site.register(Purpose)

admin.site.register(Vehicle)

admin.site.register(Driver_rating)

admin.site.register(Trip)


class Hitch_RequestAdmin(admin.ModelAdmin):
    list_display = ('pax_approved','display_trip', 'get_driver', 'hitcher', 'depart_date', 'depart_time')

    def display_trip(self, obj):
        return obj.trip if obj.trip else "No drivers yet"
    display_trip.short_description = 'Trip'
    
    def get_driver(self, obj):
        if obj.trip:
            return obj.trip.driver.username
        else:
            return "-----"
    get_driver.short_description = 'Driver'

admin.site.register(Hitch_Request, Hitch_RequestAdmin)

admin.site.register(Message)