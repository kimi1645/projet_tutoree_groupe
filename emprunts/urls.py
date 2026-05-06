from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.liste_emprunt, name= "listeEmprunt"  ),
    path('retourner/<int:id>/', views.retourner_emprunt, name='retournerEmprunt'),
    path('recherche/',views.recherche,name='search'), 
]
