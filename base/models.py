from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __unicode__(self):
        return self.first_name
    
