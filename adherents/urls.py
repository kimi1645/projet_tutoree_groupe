from django.urls import path
from . import views as adherent_views


urlpatterns = [
    path("", adherent_views.liste_adherents, name="listeAdherent"),
    path("ajouter/", adherent_views.ajouter_adherent, name="ajouterAdherent"),
    path("modifier/<str:id>/", adherent_views.modifier_adherent, name="modifierAdherent"),
    path("verification/", adherent_views.verification, name="verification"),
    path("inscription/", adherent_views.inscription, name="inscription"),
    path("reservation", adherent_views.reservation_avec_detail, name="reservation")
]