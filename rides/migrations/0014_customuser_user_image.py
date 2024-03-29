# Generated by Django 4.2.9 on 2024-01-15 17:46

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0013_alter_customuser_contactable'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_image',
            field=cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image'),
        ),
    ]
