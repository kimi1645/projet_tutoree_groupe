from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from adherents.models import Adherent
from livres.models import Livre
from .models import Emprunt
from .forms import EnregistrementRetourEmprunt

@login_required
def liste_emprunt(request):
    emprunts = Emprunt.objects.filter(statut='Non retourné').select_related('reservation__adherent', 'bibliothecaire').prefetch_related('reservation__ligneReservation__livre').order_by('-date_emprunt')[:10]#On limite la liste à dix
    return render (request, 'emprunts/list.html' ,{"emprunts" : emprunts })



@login_required
def retourner_emprunt(request, id):
    emprunt = get_object_or_404(Emprunt, id=id)
    if request.method == "POST":
        form = EnregistrementRetourEmprunt(request.POST, instance=emprunt)
        if form.is_valid():
            emprunt = form.save(commit=False)
            emprunt.statut = "Retourné"#On met à jour le statut
            emprunt.save()#On enreistre le changement
            return redirect('listeEmprunt')
        else:
            return HttpResponse("Formulaire invalide")
    else:
        form = EnregistrementRetourEmprunt(instance=emprunt)
        return render(request, "emprunts/retour_emprunt.html", {
            'form' : form,
            'emprunt' : emprunt#Données concernant l'emprunt
        })



@login_required
def recherche(request):
    
    query = request.GET.get('q','').strip()
    if not query:
        return redirect('listeEmprunt')
    resultats_livres=Livre.objects.none()
    resultats_emprunts=Emprunt.objects.none()
    resultats_adherents=Adherent.objects.none()
    # si c'est une seule lettre cad commence par...
    if len(query) ==1:
        lookup_livres =Q(reference__istartswith=query)|Q(titre__istartswith=query)
            
    
    # Si la requête est une phrase
    else:
        lookup_livres=Q(reference__icontains=query)|Q(titre__icontains=query)|Q(auteur__icontains=query)
                
        resultats_livres=Livre.objects.filter(lookup_livres)
        lookup_adherents =Q(nom__icontains=query)|Q(prenom__icontains=query)
        resultats_adherents=Adherent.objects.filter(lookup_adherents)

        resultats_emprunts=Emprunt.objects.filter(Q(reservation__ligneReservation__livre__reference__in=resultats_livres)|Q(reservation__adherent__nom__in=resultats_adherents)|Q(reservation__adherent__prenom__in=resultats_adherents))
    context = {
        'emprunts':resultats_emprunts,
        'query' : query,
        'nb_resultat' : resultats_emprunts.count()
    }
    return render(request,'emprunts/list.html',context)
    
            