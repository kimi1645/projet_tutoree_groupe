from django.contrib.auth.forms import AuthenticationForm
from django import forms


#Créer une formulaire d'authentification qui hérite de AuthenticationForm
class FormulaireAuthentification(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'ex: john_doe',
        'pattern' : "[0-9a-fA-F]{4,8}",
        'class' : 'form-control'
    }),label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control'
    }), label="Mots de passe")