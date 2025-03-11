from django.dispatch import receiver
from django.db.models.signals import post_save
from . import models


@receiver(post_save, sender=models.MyUser)
def create_profile(sender, instance, created,**kwargs):
    if created:
        models.Profile.objects.create(user=instance)