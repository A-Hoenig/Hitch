from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.utils.html import format_html
from django.core.validators import RegexValidator
from hitch import settings
from cloudinary.models import CloudinaryField

# Constants for dropdowns
TRIP_STATUS = ((0, "Confirmed"), (1, "Completed"), (2, "Cancelled"))

GENDER = (
    (0, "Female"),
    (1, "Male"),
    (2, "Non Binary"),
    (3, "Prefer not to say"))

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

VEHICLE_STATUS = (
    (True, "Active"),
    (False, "Not Active"),
    )

# Create your models here.
class CustomUser(AbstractUser):
    """
    Stores additional info about user related to
    :model:`auth.User`.
    """
    gender = models.IntegerField(choices=GENDER, default=3)
    DOB = models.DateField(
        verbose_name="Birthday",
        default=None,
        blank=True, null=True)
    adr_street = models.CharField(
        max_length=100,
        verbose_name="Street",
        blank=True, null=True)
    adr_city = models.CharField(
        max_length=50,
        verbose_name="City",
        blank=True, null=True)
    adr_zip = models.CharField(
        max_length=10,
        verbose_name="ZIP Code",
        blank=True, null=True)
    adr_country = models.CharField(
        max_length=50,
        verbose_name="Country",
        blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    DL_date = models.DateField(
        default=None,
        blank=True, null=True,
        verbose_name="Driver's License Date")
    contactable = models.BooleanField(choices=YES_NO, default=False)
    user_image = CloudinaryField('image', default='placeholder')
    average_driver_rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        default=0.0,
        blank=True, null=True)
    average_hitcher_rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        default=0.0,
        blank=True, null=True)


class Region(models.Model):
    """
    Stores a specific region to limit trips locally
    related to  :model: `Trip`, `Hitch_request`
    """
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    region = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.region


class Stop_Type(models.Model):
    """
    Stores the type of drop off point and a symbol to represent it
    related to :model: `Location`
    """

    stop = models.CharField(max_length=50, unique=True)
    stop_icon = models.CharField(max_length=50)

    def __str__(self):
        return self.stop


class Location(models.Model):
    """
    Stores previous locations related to 
    :model:`rides.Region`,`auth.User`
    """
    date_created = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    input_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stoptype = models.ForeignKey(
        Stop_Type,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True, blank=True)
    lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True, blank=True)
    google_id = models.CharField(
        max_length=50,
        null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} | {self.city}'


class Purpose(models.Model):
    """
    Stores trip purposes and corresponding
    font-awesome icon tag related to
    :model: `trip`, `hitch_request`
    """

    purpose = models.CharField(max_length=50, unique=True)
    purpose_icon = models.CharField(max_length=50)

    def __str__(self):
        return self.purpose


class Vehicle(models.Model):
    """
    Stores vehicle information
    related to :model:`rides.Trip` and :model:`auth.User`
    """
    date_created = models.DateTimeField(auto_now_add=True)
    make = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    type = models.IntegerField(choices=VEHICLE_TYPE, default=0)
    year = models.CharField(max_length=4, null=True, blank=True)
    engine = models.IntegerField(choices=ENGINE, default=0)
    smoking = models.IntegerField(choices=YES_NO, default=0)
    max_pax = models.PositiveIntegerField(default=1,)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True)
    operator = models.CharField(
        verbose_name="Operated by",
        max_length=50,
        null=True, blank=True)
    status = models.BooleanField(choices=VEHICLE_STATUS, default=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.get_type_display()})"


class User_rating(models.Model):
    """
    Stores driver ratings related to
    :model:`auth.User`
    """
    RATING_TYPE_CHOICES = (
        ('driver', 'Driver'),
        ('hitcher', 'Hitcher'),
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    rating_type = models.CharField(
        max_length=7,
        choices=RATING_TYPE_CHOICES)
    star_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    comment = models.TextField(
        max_length=300,
        null=True, blank=True)

    def __str__(self):
        return (f"{self.get_rating_type_display()}: {self.user} |"
                f" Rating: {self.star_rating} | {self.comment}")


class Trip(models.Model):
    """
    Stores a single trip related to
    :model:`auth.User`, `region`, `vehicle`, `purpose`, `location`
    """

    date_created = models.DateTimeField(
        auto_now_add=True,
        db_index=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True)
    depart_date = models.DateField()
    trip_status = models.IntegerField(
        choices=TRIP_STATUS,
        default=0,
        null=True, blank=True)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True)
    max_hitch = models.PositiveIntegerField(default=1)
    depart = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="depart",)
    destination = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="destination",)
    depart_time = models.TimeField()
    expected_duration = models.DurationField(null=True, blank=True)
    expected_arrival_time = models.TimeField(null=True, blank=True)
    depart_window = models.DurationField(null=True, blank=True)
    note = models.CharField(max_length=150, null=True, blank=True)
    direction = models.BooleanField(choices=DIRECTION, default=False)
    return_time = models.TimeField(null=True, blank=True)
    recurring = models.BooleanField(choices=YES_NO, default=0)
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)
    purpose = models.ForeignKey(
        Purpose,
        on_delete=models.SET_DEFAULT,
        default="deleted")
    suggested_tip = models.FloatField(
        null=True, blank=True)
    pickup_radius = models.IntegerField(
        null=True, blank=True, default=2,)
    max_detour_dist = models.IntegerField(
        null=True, blank=True, default=5)

    class Meta:
        ordering = ["-depart_date"]

    def __str__(self):
        return f"{self.depart} --to-- {self.destination}"


class Hitch_Request(models.Model):
    """
    Stores a request related to
    :model:`rides.Trip`,`rides.Region`,
    `auth.User`, `rides.purpose`, `rides.location`
    """
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="hitch_requests")
    hitcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True)
    depart = models.ForeignKey(
        Location, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="request_depart")
    destination = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    depart_date = models.DateField()
    depart_time = models.TimeField(null=True, blank=True)
    depart_window = models.DurationField(null=True, blank=True)
    smoking = models.BooleanField(choices=YES_NO, default=False)
    note = models.TextField(null=True, blank=True)
    direction = models.IntegerField(choices=DIRECTION, default=0)
    recurring = models.IntegerField(null=True, blank=True)
    purpose = models.ForeignKey(
        Purpose,
        on_delete=models.SET_DEFAULT,
        default=None, null=True)
    pax_approved = models.BooleanField(choices=YES_NO, default=False)
    trip_rating = models.IntegerField(null=True, blank=True)
    trip_comment = models.CharField(max_length=50, null=True, blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ["-depart_date"]

    def __str__(self):
        return (
            f"{self.depart_date} at {self.depart_time} | "
            f"from {self.depart} to {self.destination}"
        )


class Message(models.Model):
    """
    Stores in app messages between users
    related to  :model:`rides.Trip`, `auth.User`
    and :model:`hitch_request`
    """
    date_created = models.DateTimeField(
        auto_now_add=True,
        db_index=True)
    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    hitch_request = models.ForeignKey(
        Hitch_Request,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="sender")
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="receiver")
    content = models.CharField(
        max_length=500,
        null=True, blank=True)
    was_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        # need to get driver and hitcher from FK relationship now
        # trip might not exist yet so has to be dealt with
        driver = self.trip.driver if self.trip else "No Trip yet"
        hitcher = (
            self.hitch_request.hitcher
            if self.hitch_request
            else "No Hitch Request")
        sender = self.sender
        receiver = self.receiver

        return f"{sender} -> {receiver} | {self.content}"
