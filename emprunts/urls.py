from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.liste_emprunt, name= "listeEmprunt"  ),
    path('ajouter/', views.enregistrer_emprunt, name='enregistrerEmprunt'),
    path('retourner/<int:id>/', views.retourner_emprunt, name='retournerEmprunt') 
]
