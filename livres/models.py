from django.db import models


CATEGORIE = [
    ('Math','Mathématique'),
    ('Physique', 'Physique'),
    ('Littérature','Littérature'),
    ('Droit', 'Droit'),
    ("Memoire de fin d'étude", "Memoire de fin d'étude"),
    ('Thèse','Thèse')
]



class Livre(models.Model):
    reference = models.CharField(primary_key=True)
    titre = models.CharField(max_length=150)
    auteur = models.CharField(max_length=150)
    categorie = models.CharField(choices=CATEGORIE)
    quantite = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.reference} - {self.titre}"
