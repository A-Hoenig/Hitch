# Generated by Django 4.2.9 on 2024-01-14 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0011_alter_vehicle_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='smoking',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]