from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse


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
class User_Profile(models.Model):
    """
    Extends the django User model with additional info :model:`auth.User`
    first_name, last_name, email, username inherited from auth.User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.IntegerField(choices=GENDER, default=3)
    DOB = models.DateTimeField()
    adr_street = models.CharField(max_length=100)
    adr_city = models.CharField(max_length=50)
    adr_zip = models.CharField(max_length=10)
    adr_country = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    DL_date = models.DateTimeField()
    contactable = models.IntegerField(choices=YES_NO, default=0)

# add User_profile data if normal User is updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()


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
    input_by = models.ForeignKey(User, on_delete=models.CASCADE)
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



