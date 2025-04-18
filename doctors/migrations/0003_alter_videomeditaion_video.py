# Generated by Django 5.1.6 on 2025-04-07 18:14

import cloudinary.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_videomeditaion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomeditaion',
            name='video',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3'])], verbose_name='audio'),
        ),
    ]
