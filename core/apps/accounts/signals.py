from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from . import models


@receiver(post_save, sender=models.MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)


@receiver(pre_save, sender=models.Checkout)
def my_address_pre_save_handler(sender, instance, **kwargs):
    if instance.is_default:
        old_checkout = models.Checkout.objects.filter(
            user_profile=instance.user_profile, is_default=True
        )
        if old_checkout:
            old_checkout.update(is_default=False)
