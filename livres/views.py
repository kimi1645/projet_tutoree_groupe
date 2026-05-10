from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render , redirect
from .models import Livre
from .forms import LivreForm, LivreModificationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from bibliotheque.utils import get_user_role

@login_required
def liste_livre(request) :
    livres = Livre.objects.all()
    return render (request , 'livres/list.html' , {'livres' : livres})

@login_required
def ajouter_livre(request):
    if  get_user_role(request.user)['role'] == 'adherent':
        return HttpResponseForbidden("Vous n'avez pas la permission nécessaire pour cette page.")
    else:
        form = LivreForm(request.POST or None)
        if form.is_valid() : 
            form.save()
            return redirect("liste_livre")
        return render(request , 'livres/formulaire.html' , {'form' : form})

@login_required
def recherche(request) :
    query = request.GET.get('q','').strip()
    if not query:
        return redirect('liste_livre')
    else:
        nbre_resultat = 0
        livre_lookup = Q(categorie__icontains=query) | Q(titre__icontains=query) | Q(auteur__icontains=query) 
        livres =  Livre.objects.filter(livre_lookup)
        context = {
            'livres' : livres,
            'nbre_resultat' : livres.count(),
            'query' : query
        }
        return render (request, 'livres/list.html', context)

@login_required
def modifier_livres(request , ref) :
    if get_user_role(request.user)['role'] == 'bibliothecaire':
        livre = get_object_or_404(Livre , pk=ref)
        form = LivreModificationForm(request.POST or None , instance=livre)
        if form.is_valid() :
            form.save()
            return redirect('liste_livre')
        return render(request , 'livres/modifier_livre.html' , {'form': form})
    else:
        return HttpResponseForbidden("Vous n'avez pas la permission nécessaire pour cette page.")

def supprimer_livres(request , ref) :
    livre = get_object_or_404(Livre , pk=ref)
    if request.method == 'POST' :
        livre.delete()
        return redirect('liste_livre')
    else:
        return render(request, 'livres/confirmation_suppression.html', {
            'livre' : livre
        })