# Generated by Django 4.2.9 on 2024-01-15 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0012_alter_vehicle_smoking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='contactable',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=0),
        ),
    ]
