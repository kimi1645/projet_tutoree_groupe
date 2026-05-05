from django.contrib import admin
from django.urls import path
from .import views 

urlpatterns = [
    path('', views.liste_livre , name="liste_livre"),#le liste any @ views
    path('ajouter/', views.ajouter_livre , name="ajouter_livre"),
    path('recherche/', views.recherche, name='recherche'),
]