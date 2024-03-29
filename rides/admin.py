from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from .models import (
    Region,
    Location,
    CustomUser,
    Purpose,
    Vehicle,
    User_rating,
    Trip,
    Hitch_Request,
    Stop_Type,
    Message)


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name',
        'gender', 'DOB', 'average_driver_rating', 'average_hitcher_rating'
        )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
                'user_image')}),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'gender',
                'average_driver_rating',
                'average_hitcher_rating')}),
        ('Hitch Driver Info', {
            'fields': (
                'DOB',
                'DL_date',
                'adr_street',
                'adr_city',
                'adr_zip',
                'adr_country',
                'phone',
                'contactable')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
                'date_joined')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'username',
                'password1',
                'password2')
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'gender',
                'average_driver_rating',
                'average_hitcher_rating')
        }),
        ('Hitch Driver Info', {
            'fields': (
                'DOB',
                'DL_date',
                'adr_street',
                'adr_city',
                'adr_zip',
                'adr_country',
                'phone',
                'contactable')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions')
        }),
        ('Important dates', {
            'fields': (
                'last_login',
                'date_joined')
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'date_created')
    list_filter = ['region', 'date_created']


admin.site.register(Region, RegionAdmin)


class CustomLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'name', 'city', 'date_created', 'input_by')
    list_filter = ['region', 'date_created']


admin.site.register(Location, CustomLocationAdmin)


class StopTypeAdmin(admin.ModelAdmin):
    list_display = ('stop', 'stop_icon')

    def icon_display(self, obj):
        return mark_safe(obj.stop_icon)
    icon_display.short_description = 'Icon'


admin.site.register(Stop_Type, StopTypeAdmin)

admin.site.register(Purpose)

admin.site.register(Vehicle)

admin.site.register(User_rating)


class TripAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'driver',
        'date_created_DMY',
        'depart_date',
        'depart_time',
        'depart',
        'destination',)
    list_filter = ('region', 'driver',)

    # create some more readable date/time formats for datatable
    def date_created_DMY(self, obj):
        return obj.date_created.strftime("%d.%m.%Y (%H:%M)")
    date_created_DMY.short_description = "submitted"

    def depart_date_DM(self, obj):
        return obj.date_created.strftime("%d.%b")
    depart_date_DM.short_description = "Leave"

    def depart_time_HHMM(self, obj):
        return obj.date_created.strftime("%H:%M")
    depart_time_HHMM.short_description = "At"


admin.site.register(Trip, TripAdmin)


class Hitch_RequestAdmin(admin.ModelAdmin):
    # get data from linked trip via trip.id
    def display_trip(self, obj):
        return obj.trip if obj.trip else "No drivers yet"
    display_trip.short_description = 'Linked Trip Details'

    def get_driver(self, obj):
        if obj.trip:
            return obj.trip.driver.username
        else:
            return "-----"
    get_driver.short_description = 'Driver'

    # create some more readable date/time formats for datatable
    def date_created_YMD(self, obj):
        return obj.date_created.strftime("%d.%m.%Y (%H:%M)")
    date_created_YMD.short_description = "submitted"

    def depart_date_YMD(self, obj):
        return obj.date_created.strftime("%d.%b")
    depart_date_YMD.short_description = "Leave"

    def depart_time_HHMM(self, obj):
        return obj.date_created.strftime("%H:%M")
    depart_time_HHMM.short_description = "At"

    list_display = (
        'id',
        'date_created_YMD',
        'is_public',
        'pax_approved',
        'display_trip',
        'get_driver',
        'hitcher',
        'depart_date_YMD',
        'depart_time_HHMM')
    list_filter = ('region', 'is_public', 'hitcher')


admin.site.register(Hitch_Request, Hitch_RequestAdmin)

admin.site.register(Message)
