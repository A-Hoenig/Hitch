# Generated by Django 4.2.9 on 2024-01-13 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0009_vehicle_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'Not Active')], default=0),
        ),
    ]
