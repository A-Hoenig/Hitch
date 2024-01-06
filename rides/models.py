from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.utils.html import format_html
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


class Region(models.Model):
    """
    Stores a specific region to limit trips locally 
    related to  :model: ``
    """
    date_created = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.region

class Location(models.Model):
    """
    Stores previous locations related to :model:`rides.Region`,`auth.User`
    """
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    input_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stop_type = models.IntegerField(choices=STOP_TYPE, default=0)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    google_id = models.CharField(max_length=50, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.city}, {self.street} ({self.get_stop_type_display()})'

class Purpose(models.Model):
    """
    Stores trip purposes and corresponding font-awesome icon tag related to  :model:``
    """
    
    purpose = models.CharField(max_length=50, unique=True)
    purpose_icon = models.CharField(max_length=50)
    

    def __str__(self):
        return self.purpose

class Vehicle(models.Model):
    """
    Stores vehicle related to :model:`rides.Trip` and :model:`auth.User`
    """
    date_created = models.DateTimeField(auto_now_add=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    type = models.IntegerField(choices=VEHICLE_TYPE, default=0)
    year = models.CharField(max_length=4)
    engine = models.IntegerField(choices=ENGINE, default=0)
    smoking = models.IntegerField(choices=YES_NO, default=0)
    max_pax = models.IntegerField(
        default=1,
     )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    operator = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.get_type_display()}), owned by {self.owner}"

class Driver_rating(models.Model):
    """
    Stores driver ratings related to  :model:`rides.Trip` and :model:`auth.User`
    """
    date_created = models.DateTimeField(auto_now_add=True)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    star_rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1,
    )
    comment = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"Driver: {self.driver} | Rating: {self.star_rating} | {self.comment}"

class Trip(models.Model):
    """
    Stores a single trip related to 
    :model:`auth.User`, `region`, `vehicle`, `purpose`, `location`
    """
    
    date_created = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    trip_date = models.DateField()
    trip_status = models.IntegerField(choices=TRIP_STATUS, default=0)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    max_hitch = models.IntegerField(default=0,)
    depart = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="depart")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE)
    depart_time = models.TimeField()
    expected_duration = models.DurationField(null=True, blank=True)
    expected_arrival_time = models.TimeField(null=True, blank=True)
    depart_window = models.DurationField(null=True, blank=True)
    note = models.CharField(max_length=150, null=True, blank=True)
    direction = models.IntegerField(choices=DIRECTION, default=0)
    return_time = models.TimeField(null=True, blank=True)
    recurring = models.IntegerField(choices=YES_NO, default=0)
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
    suggested_tip = models.FloatField(null=True, blank=True)
    pickup_radius = models.IntegerField(default=2,)
    max_detour_dist = models.IntegerField(default=5,)

    class Meta:
        ordering = ["-trip_date"]

    def __str__(self):
        return f"{self.trip_date} at {self.depart_time} | from {self.depart} --to-- {self.destination}"
    

class Request(models.Model):
    """
    Stores a trip request related to  
    :model:`rides.Trip`,`rides.Region`,`auth.User`, `rides.purpose`, `rides.location`
    """
    date_created = models.DateTimeField(auto_now_add=True)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
    hitcher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    depart = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name="request_depart")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    depart_date = models.DateTimeField()
    depart_time = models.DateTimeField(null=True, blank=True)
    depart_window = models.DurationField(null=True, blank=True)
    smoking = models.IntegerField(choices=YES_NO, default=0)
    note = models.TextField(null=True, blank=True)
    direction = models.IntegerField(choices=DIRECTION, default=0)
    recurring = models.IntegerField(null=True, blank=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["-depart_date"]

    def __str__(self):
        return f"{self.date} at {self.depart_time} | from {self.depart} to {self.destination}"


class Message(models.Model):
    """
    Stores in app messages between users related to  :model:`rides.Trip`,auth.User
    """
    date_created = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.sender} -> {self.receiver} | {self.message}"