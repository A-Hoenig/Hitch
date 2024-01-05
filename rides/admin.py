from django.contrib import admin
from .models import Profile, Region, Location


# Register your models here.
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    pass


