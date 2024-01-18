# Generated by Django 4.2.9 on 2024-01-17 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0015_alter_trip_recurring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='depart_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='request',
            name='depart_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='smoking',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]