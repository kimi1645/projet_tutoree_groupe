from django.db import models
from django.contrib.auth.models import User
from livres.models import Livre

FONCTIONS = [
    ('Etudiant','Etudiant'),
    ('Formateur', 'Formateur'),
    ('Employé', 'Employé')
]


# Create your models here.
class Adherent(models.Model):
    matricule = models.CharField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=100)
    #unique = true  Ceci evite la duplication des adresse email
    email = models.EmailField(unique=True)
    fonctions = models.CharField(choices=FONCTIONS)


    def __str__(self):
        return f"{self.matricule} -- {self.nom} {self.prenom}"



class CompteAdherent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personne = models.OneToOneField(Adherent, on_delete=models.CASCADE)


class Reservation(models.Model):
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    date_reservation = models.DateField(auto_now_add=True)
    statut = models.CharField(choices=[
        ('En attente', 'En attente'),
        ('Validée', 'Validée'),
        ('Refusée', 'Refusée'),
    ], default='En attente')
    valider_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_validation = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.pk}"


class DetailReservation(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='ligneReservation')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, limit_choices_to={
        'quantite__gt': 0
    })
    quantite = models.PositiveIntegerField(default=1)