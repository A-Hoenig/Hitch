# Generated by Django 4.2.9 on 2024-01-06 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0003_vehicle_trip_request_driver_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='region',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]