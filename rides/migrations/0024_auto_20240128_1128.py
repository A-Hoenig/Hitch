# Generated by Django 3.2.13 on 2024-01-28 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0023_auto_20240126_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='location',
            name='stoptype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rides.stop_type'),
        ),
    ]