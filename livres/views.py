from django.shortcuts import render , redirect
from .models import Livre
from .forms import LivreForm

def liste_livre(request) :
    livres = Livre.objects.all()
    return render (request , 'livres/list.html' , {'livres' : livres})


def ajouter_livre(request):
    form = LivreForm(request.POST or None)
    if form.is_valid() : 
        form.save()
        return redirect("liste_livre")
    return render(request , 'livres/formulaire.html' , {'form' : form})

def recherche(request) :
    query = request.GET.get('livres')
    livres =  Livre.objects.filter(titre__icontains=query)
    context = {
        'livres' : livres
    }
    #return render (request, 'resultat_recherche.html', context)