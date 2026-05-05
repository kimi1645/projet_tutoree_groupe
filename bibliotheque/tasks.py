from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from emprunts.models import Emprunt
from django.conf import settings

def envoyer_rappels():
    ajourd_hui = timezone.now().date()#Date aujourd'hui
    dans_3_jours = ajourd_hui + timedelta(days=3)#3 jours avant la date_limite

    #On recupère tous les emprunts non retourné où la date limite est dans 3 jours
    emprunts_bientot = Emprunt.objects.filter(
        statut='Non retourné',
        date_limite=dans_3_jours
    )

    #on envoi un email à chaque emprunteur
    for emprunt in emprunts_bientot:
        send_mail(
            subject='Rappel- Retour de livre',
            message=f'Bonjour {emprunt.adherent.nom} {emprunt.adherent.prenom}, votre livre "{emprunt.ref_livre.titre}" doit être retounré dans 3 jours.',
            from_email=settings.EMAIL_FROM,
            recipient_list=[emprunt.adherent.email]
        )


    
    #Tous les emprunts en retard
    emprunts_retard = Emprunt.objects.filter(
        statut='Non retourné',
        date_limite__lt=ajourd_hui
    )

    emprunts_retard.update(statut='En retard')#On met à jour le statut

    #Envoie d'une email de notification
    for emprunt in emprunts_retard:
        send_mail(
            subject='Retard- Retour de livre',
            message=f'Bonjour {emprunt.adherent.nom} {emprunt.adherent.prenom}, votre livre "{emprunt.ref_livre.titre}" est en retard depuis le {emprunt.date_limite}.Veuillez le deposez auprès de la bibliothèque.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[emprunt.adherent.email]
        )