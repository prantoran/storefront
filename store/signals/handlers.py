from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer

@receiver(post_save, sender=settings.AUTH_USER_MODEL) # AUTH_USER_MODEL decouples User from core
def create_customer_for_new_user(sender, **kwargs): # a signal handler
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])