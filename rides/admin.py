from django.contrib import admin
from .models import User_Profile, Region, Location


# Register your models here.
@admin.register(User_Profile)
class User_data(admin.ModelAdmin):
    pass


