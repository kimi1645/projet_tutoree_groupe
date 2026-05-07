from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render , redirect
from .models import Livre
from .forms import LivreForm
from django.db.models import Q

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
    query = request.GET.get('q','').strip()
    if not query:
        return redirect('liste_livre')
    else:
        nbre_resultat = 0
        livre_lookup = Q(reference__icontains=query) | Q(titre__icontains=query) | Q(auteur__icontains=query) 
        livres =  Livre.objects.filter(livre_lookup)
        context = {
            'livres' : livres,
            'nbre_resultat' : livres.count(),
            'query' : query
        }
        return render (request, 'livres/list.html', context)


def modifier_livres(request , ref) :
    livre = get_object_or_404(Livre , pk=ref)
    form = LivreForm(request.POST or None , instance=livre)
    if form.is_valid() :
        form.save()
        return redirect('liste_livre')
    return render(request , 'livres/modifier_livre.html' , {'form': form})


def supprimer_livres(request , ref) :
    livre = get_object_or_404(Livre , pk=ref)
    if request.method == 'POST' :
        livre.delete()
        return redirect('liste_livre')
    else:
        return render(request, 'livres/confirmation_suppression.html', {
            'livre' : livre
        })