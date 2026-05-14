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
    
    # Conditions de recherche
    #Si l'utilisateur ne saisie qu'un seul caractère
    if len(query) == 1:
        lookup_livres = Q(reference__istartswith=query) | Q(titre__istartswith=query)
        lookup_adherents = Q(nom__istartswith=query) | Q(prenom__istartswith=query)
    #S'il saisie plus d'un caractère
    else:
        lookup_livres = Q(reference__icontains=query) | Q(titre__icontains=query) | Q(auteur__icontains=query)
        lookup_adherents = Q(nom__icontains=query) | Q(prenom__icontains=query) | Q(matricule__icontains=query)
    
    # Filtrer les emprunts par:
    # - Référence/titre du livre OU
    # - Nom/prénom/matricule de l'adhérent OU
    # - Numéro de réservation (si query est un entier)
    filter_conditions = (
        Q(reservation__ligneReservation__livre__reference__icontains=query) |
        Q(reservation__ligneReservation__livre__titre__icontains=query) |
        Q(reservation__ligneReservation__livre__auteur__icontains=query) |
        Q(reservation__adherent__nom__icontains=query) |
        Q(reservation__adherent__prenom__icontains=query) |
        Q(reservation__adherent__matricule__icontains=query)
    )
    
    # Ajouter la recherche par ID de réservation si query est un entier
    try:
        reservation_id = int(query)
        filter_conditions |= Q(reservation__id=reservation_id)
    except ValueError:
        pass
    
    resultats_emprunts = Emprunt.objects.filter(filter_conditions).select_related(
        'reservation__adherent', 'bibliothecaire'
    ).prefetch_related(
        'reservation__ligneReservation__livre'#Accèderaux livres liés à l'emprunt
    ).distinct().order_by('-date_emprunt')
    
    context = {
        'emprunts': resultats_emprunts,
        'query': query,
        'nb_resultat': resultats_emprunts.count()
    }
    return render(request,'emprunts/list.html',context)
    
            