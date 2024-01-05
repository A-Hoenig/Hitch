from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from hitch import settings


# Constants for dropdowns
TRIP_STATUS = ((0, "Confirmed"), (1, "Completed"), (2, "Cancelled"))
GENDER = ((0, "Female"), (1, "Male"), (2, "Non Binary"), (3, "Prefer not to say"))
DIRECTION = ((0, "One Way"), (1, "Return Trip"))
YES_NO = ((1, "Yes"), (0, "No"))
ENGINE = (
    (0, "Gasoline"), 
    (1, "Diesel"), 
    (2, "Hybrid"), 
    (3, "Electric"),
    (4, "LNG"),
    (5, "OTHER")
    )
VEHICLE_TYPE = (
    (0, "Sedan"), 
    (1, "SUV"), 
    (2, "Roadster"), 
    (3, "Minvan"),
    (4, "Truck"),
    (5, "Bus"),
    (6, "LKW")
    )
STOP_TYPE = (
    (0, "Address"), 
    (1, "Bus Stop"), 
    (2, "Intersection"), 
    (3, "Parking Lot"),
    (4, "Gas Station")
    )

# Create your models here.
class CustomUser(AbstractUser):
    gender = models.IntegerField(choices=GENDER, default=3)
    DOB = models.DateField(verbose_name="Birthday", default=None, blank=True, null=True)
    adr_street = models.CharField(max_length=100, verbose_name="Street")
    adr_city = models.CharField(max_length=50, verbose_name="City")
    adr_zip = models.CharField(max_length=10, verbose_name="ZIP Code")
    adr_country = models.CharField(max_length=50, verbose_name="Country")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    DL_date = models.DateField(default=None, blank=True, null=True, verbose_name="Driver's License Date")
    contactable = models.IntegerField(choices=YES_NO, default=0)

# class Profile(models.Model):
#     """
#     Extends the django User model with additional info :model:`auth.User`
#     first_name, last_name, email, username inherited from auth.User
#     """
#     user = models.OneToOneField(User, on_delete=models.PROTECT,)
#     gender = models.IntegerField(choices=GENDER, default=3)
#     DOB = models.DateField('Date', null=True, blank=True)
#     adr_street = models.CharField(max_length=100, verbose_name="Street")
#     adr_city = models.CharField(max_length=50, verbose_name="City")
#     adr_zip = models.CharField(max_length=10, verbose_name="ZIP Code")
#     adr_country = models.CharField(max_length=50, verbose_name="Country")
#     phone = models.CharField(max_length=15, verbose_name="Phone Number")
#     DL_date = models.DateField(verbose_name="Driver's License Date")
#     contactable = models.IntegerField(choices=YES_NO, default=0)

#     def __str__(self):
#         return self.user.username

class Region(models.Model):
    """
    Stores a specific region to limit trips locally 
    related to  :model: ``
    """
    date_created = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"Operating Region: {self.region}"

class Location(models.Model):
    """
    Stores previous locations related to :model:`rides.Region`,`auth.User`
    """
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    input_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stop_type = models.IntegerField(choices=YES_NO, default=0)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    google_id = models.CharField(max_length=50)
    note = models.TextField()


