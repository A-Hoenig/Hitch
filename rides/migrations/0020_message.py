# Generated by Django 3.2.13 on 2024-01-25 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0019_auto_20240125_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
                ('was_read', models.BooleanField(default=False)),
                ('hitch_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='rides.hitch_request')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='rides.trip')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
