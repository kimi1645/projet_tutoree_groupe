from django.urls import path
from . import views as adherent_views


urlpatterns = [
    path("", adherent_views.liste_adherents, name="listeAdherent"),
    path("ajouter/", adherent_views.ajouter_adherent, name="ajouterAdherent"),
    path("modifier/<str:id>/", adherent_views.modifier_adherent, name="modifierAdherent"),
]