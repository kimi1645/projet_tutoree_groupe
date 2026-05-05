from django.db.models import Sum
from livres.models import Livre
from adherents.models import Adherent
from emprunts.models import Emprunt


#on définit cette fonction context_processeurs parce que on a besoin de renvoyer ces données
#à la template de base pour eviter de créer une fonction views pour chaque application
#Cette fonction dashboards_stats s'execute automatiquement à chaque requête et envoie les données à toutes les templates
def dashboard_stats(request):
        #Total livre par titre
    total_livres = Livre.objects.aggregate(total=Sum('quantite'))['total'] or 0 #calculé le nombre des livres
    #disponibles en additionnant les quantités et en stockant le resulat dans une variable total
    #aggregate retourne un dictionnaire  {'total' : total }
    titres_differents = Livre.objects.count() #On compte les différentes titres du livre enregistrer


    #Totals adhérents
    total_adherents = Adherent.objects.count()
    #Membres actifs
    #emprunt__statut = requette join Adherent --> Emprunt --> statut
    # .distinct() evite le doublons
    membres_actifs = Adherent.objects.filter(emprunt__statut='Non retourné').distinct().count()
    print(membres_actifs)

    #Emprunts en cours
    #Filtration des emprunts avec attribus statut = 'Non retourné
    emprunts_en_cours = Emprunt.objects.filter(statut='Non retourné').count()
    return {
        'total_livres' : total_livres,
        'titres_differents' : titres_differents,
        'total_adherents' : total_adherents,
        'membres_actifs' : membres_actifs,
        'emprunts_en_cours' : emprunts_en_cours
    }

    