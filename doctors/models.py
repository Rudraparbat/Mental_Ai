from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.core.validators import FileExtensionValidator

class Mentaluser(models.Model) :
    username = models.CharField(max_length=255) 
    email = models.EmailField(max_length=255)
    set_password = models.CharField(max_length=255)
    def __str__(self):
        return self.username
    

# video-Meditation Trying Model Where we save video data

class VideoMeditaion(models.Model) :
    video_description = models.TextField()
    video_partial_id = CloudinaryField('audio',
        resource_type='raw',  # MP3s are uploaded as raw files
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],  # Restrict to MP3
        null=True,
        blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_description