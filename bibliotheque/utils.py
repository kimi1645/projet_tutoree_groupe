from django.contrib.auth.models import User
from adherents.models import CompteAdherent

def get_user_role(user):
    if not user or not user.is_authenticated:
        return None
    try:
        compte = user.compteadherent
        return{
            'role' : 'adherent',
            'personne' : compte.personne,
        }
    except CompteAdherent.DoesNotExist:
        return{
            'role' : 'bibliothecaire',
            'compte' : None,
            'personne' : None
        }