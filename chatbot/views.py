from django.shortcuts import render
from django.http import HttpResponseForbidden
import json
from groq import Groq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bibliotheque.utils import get_user_role
from livres.models import Livre
from adherents.models import Reservation
from emprunts.models import Emprunt
from decouple import config
from .models import HistoriqueChat
from django.contrib.auth.decorators import login_required

#Récupération de toutes les données nécessaires 
def get_context_bibliotheque(adherent):
    #Données concernant les réservations et détails réservations
    reservations = Reservation.objects.prefetch_related('ligneReservation').filter(
        adherent=adherent
    ).values('statut','date_reservation')

    #DOnnées concernant l'emprunt
    emprunts = Emprunt.objects.filter(
        reservation__adherent=adherent,
        statut='Non retourné'
    ).values(
        'reservation__ligneReservation__livre__titre',
        'date_limite'
    )

    # Liste de toutes les livres 
    livres = Livre.objects.values('titre','auteur','categorie','quantite')

    # On retourne une chaîne de caractère qui contient le requête à envoyé au client GROK
    return f"""
    Tu es un assistant pour une bibliothèque universitaire.
    Tu aides l'adhérent {adherent.nom} {adherent.prenom}.

    Ses emprunts en cours :
    {list(emprunts)}

    Ses réservations :
    {list(reservations)}

    Livres disponibles :
    {list(livres)}

    Règles :
    - Réponds uniquement en français
    - Réponds uniquement aux questions liées à la bibliothèque
    - Sois poli et concis
    """


@csrf_exempt
@login_required
def chatbot(request):
    if get_user_role(request.user)['role'] == 'bibliothecaire':
        return HttpResponseForbidden("Vous n'avez pas la permission nécessaire pour cette page.")
    if request.method == 'POST':
        data     = json.loads(request.body)
        question = data.get('message', '')#Récupération du message
        adherent = request.user.compteadherent.personne#Récuperation de l'adherent connecté

        #Sauvegarder message utilisateur
        HistoriqueChat.objects.create(
            adherent = adherent,
            role     = 'user',
            message  = question
        )

        # Récupérer les 10 derniers messages pour le contexte
        historique = HistoriqueChat.objects.filter(
            adherent=adherent
        ).order_by('-date')[:10][::-1]
        #::-1 renverser l'ordre de l'historique

        # Construire les messages pour Groq
        messages = [
            {'role': 'system', 'content': get_context_bibliotheque(adherent)}
        ]

        # Ajouter l'historique au contexte
        for h in historique:
            messages.append({
                'role'   : 'user' if h.role == 'user' else 'assistant',
                'content': h.message
            })

        # Appel Groq
        client   = Groq(api_key=config('GROK_API_KEY'))
        response = client.chat.completions.create(
            model    = 'llama-3.1-8b-instant',
            messages = messages
        )

        reponse_bot = response.choices[0].message.content

        # Sauvegarder réponse bot
        HistoriqueChat.objects.create(
            adherent = adherent,
            role     = 'bot',
            message  = reponse_bot
        )

        return JsonResponse({'response': reponse_bot})
    return render(request, 'chatbot/chat.html')

# Charger l'historique au chargement de la page
def charger_historique(request):
    adherent  = request.user.compteadherent.personne
    historique = HistoriqueChat.objects.filter(
        adherent=adherent
    ).order_by('date')

    data = [
        {'role': h.role, 'message': h.message, 'date': str(h.date)}
        for h in historique
    ]
    #Revoie données au format json à recupérer au template chatbot/chat.html
    return JsonResponse({'historique': data})