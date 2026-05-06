from django.db.models import Sum
from livres.models import Livre
from adherents.models import Adherent, Reservation
from emprunts.models import Emprunt
from .utils import get_user_role


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
    #emprunt__statut = requette join Adherent --> Reservation --> Emprunt --> statut
    # .distinct() evite le doublons
    #Adherent qui à un emprunt en cours
    membres_actifs = Adherent.objects.filter(reservation__emprunt__statut='Non retourné').distinct().count()
    

    #Emprunts en cours
    #Filtration des emprunts avec attribus statut = 'Non retourné
    emprunts_en_cours = Emprunt.objects.filter(statut='Non retourné').count()


    role_utilisateur = get_user_role(request.user)
    if request.user.is_authenticated:
        total_reservation_effectue = 0
        reservation_validee = 0
        reservation_refusee = 0
        if role_utilisateur['role'] == 'adherent':
            total_reservation_effectue = Reservation.objects.filter(adherent=request.user.compteadherent.personne).count()
            reservation_validee = Reservation.objects.filter(adherent= request.user.compteadherent.personne, statut='Validée').count()
            reservation_refusee = Reservation.objects.filter(adherent= request.user.compteadherent.personne, statut='Refusée').count()
    
        return {
            'total_livres' : total_livres,
            'titres_differents' : titres_differents,
            'total_adherents' : total_adherents,
            'membres_actifs' : membres_actifs,
            'emprunts_en_cours' : emprunts_en_cours,
            'total_reservation_effectuee' :total_reservation_effectue,
            'reservation_validee' : reservation_validee,
            'reservation_refusee' : reservation_refusee
        }
    return {
        'default' : None
    }


def user_role(request):
    return {'user_role' : get_user_role(request.user)}

    