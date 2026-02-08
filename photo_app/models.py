from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
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

class Photo(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    title =models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="photos/")
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated tags"
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_photos",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title