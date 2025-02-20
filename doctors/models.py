from django.db import models

class Mentaluser(models.Model) :
    username = models.CharField(max_length=255) 
    email = models.EmailField(max_length=255)
    set_password = models.CharField(max_length=255)
    def __str__(self):
        return self.username
    
