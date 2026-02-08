from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OnToOneField(
        User,
        on_delete=models.CASCADE

    )
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to="profiles/", 
        blank=True,
        null=True
    )
    def __str__(self):
        return self.user.username
    
    # Automatically create a Profile when a new User is created
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)