from datetime import timedelta, datetime

from django.db import models
from livres.models import Livre
from adherents.models import Adherent
from django.contrib.auth.models import User

STATUT = [
    ('En retard', 'En retard'),
    ('Retourné', 'Retourné'),
    ('Non retourné', 'Non retourné')
]
class Emprunt(models.Model):
    #
    ref_livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    bibliothecaire = models.ForeignKey(User,on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    #datetime.now() + timedelta(days=15)  === Limitena 15 jours aorinanle nangalany azy ny date limite
    date_limite = models.DateField(default=datetime.now() + timedelta(days=15))
    date_retour = models.DateField(blank=True, null=True)
    statut = models.CharField(choices=STATUT, default='Non retourné')
    remarque = models.TextField(blank=True, default=" ")


    def __str__(self):
        return f"Emprunt n° : {self.pk}"