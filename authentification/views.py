from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

#Fonction qui gere la deconnexion d'un utilisateur
@login_required
def se_deconnecter(request):
    logout(request)
    return redirect('seConnecter')