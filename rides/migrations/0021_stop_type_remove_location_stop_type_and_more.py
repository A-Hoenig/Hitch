# Generated by Django 4.2.9 on 2024-01-19 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0020_alter_trip_options_rename_trip_date_trip_depart_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stop_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop', models.CharField(max_length=50, unique=True)),
                ('stop_icon', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='location',
            name='stop_type',
        ),
        migrations.AddField(
            model_name='location',
            name='stoptype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rides.stop_type'),
        ),
    ]
