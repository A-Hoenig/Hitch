# Generated by Django 4.2.9 on 2024-01-13 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0010_alter_vehicle_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.BooleanField(choices=[(True, 'Active'), (False, 'Not Active')], default=True),
        ),
    ]
