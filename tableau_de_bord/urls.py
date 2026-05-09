from django.urls import path
from . import views as dashboard_views

urlpatterns = [
    path("", dashboard_views.index_dashboard, name="indexDashboard"),
    path("liste_reservation/", dashboard_views.liste_reservation_avalidee, name='listeReservationAValidee'),
    path("valider/<int:id>/", dashboard_views.valider_reservation, name="validerReservation"),
    path("mes_emprunts/", dashboard_views.mes_emprunts, name="mesEmprunts")
]
