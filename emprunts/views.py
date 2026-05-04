from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from adherents.models import Adherent
from livres.models import Livre
from .models import Emprunt
from .forms import EmpruntForm, EnregistrementRetourEmprunt

@login_required
def liste_emprunt(request):
    emprunts = Emprunt.objects.all().order_by('-date_emprunt')[:10]#On limite la liste à dix
    return render (request, 'emprunts/list.html' ,{"emprunts" : emprunts })


#Fonction pour enregistrer un emprunt
@login_required
def enregistrer_emprunt(request):
    #Lors de la soumission du formulaire
    if request.method == "POST":
        form = EmpruntForm(request.POST)
        if form.is_valid():
            #On enregistre pas directement les données , on les stocke dans une variable emprunt
            emprunt = form.save(commit=False)
            #on recupere l'objet livre correspondat au réference selectionné
            livre = get_object_or_404(Livre, reference = emprunt.ref_livre.reference)
            #On vérifie que il y a encore au mois une livre en stock
            if livre.quantite < 1:#Le stock est vide quantite = 0
                form = EmpruntForm()
                return render(request, "emprunts/ajouter_emprunt.html", {
                'message' : 'Cette livre n\'est plus disponible',#Message d'erreur à affiché au utilisateur
                'form' : form 
                })
            else:#Si il y au mois une livre en stock
                emprunt.bibliothecaire = request.user#On remplie le champ bibliothecaire par l'utilisateur connecté
                emprunt.save()#on enregistre définitivement

                livre.quantite -= 1#On soustrait 1 la quantite du livre en stock
                livre.save()#on enregistre le changement

                return redirect('listeEmprunt')#Rédiriger vers la page liste des emprunts
        else:
            return HttpResponse("Formulaire invalide")
    else:
        form = EmpruntForm()
        return render(request, "emprunts/ajouter_emprunt.html", {
            'form' : form
        })



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

        resultats_emprunts=Emprunt.objects.filter(Q(ref_livre__in=resultats_livres)|Q(adherent__in=resultats_adherents))
    context = {
        'emprunts':resultats_emprunts,
        'query' : query,
        'nb_resultat' : resultats_emprunts.count()
    }
    return render(request,'emprunts/list.html',context)
    
            