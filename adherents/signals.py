from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Adherent

@receiver(post_delete, sender=Adherent)
def supprimer_user_adherent(sender, instance, **kwargs):
    if instance.user:
        instance.compteadherent.user.delete()
        