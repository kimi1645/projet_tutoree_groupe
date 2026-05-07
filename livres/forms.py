from django import forms
from .models import Livre


STYLE_DE_BASE = 'form-control m-3'
class LivreForm(forms.ModelForm) : 
    class Meta :
        model = Livre
        fields = ['reference' , 'titre' , 'auteur' , 'categorie' , 'quantite']
        widgets = {
            'reference' : forms.TextInput(attrs={
                'class' : STYLE_DE_BASE , 
                'placeholder' : 'reference'
        }),
            'titre' : forms.TextInput(attrs={
                'class' : STYLE_DE_BASE, 
                'placeholder' : 'titre'
            }),
            'auteur' : forms.TextInput(attrs={
                'class' : STYLE_DE_BASE, 
                'placeholder' : 'auteur'
            }),
            'categorie' : forms.Select(attrs={
                'class' : STYLE_DE_BASE, 
                'placeholder' : 'categorie'
            }),
            'quantite' : forms.TextInput(attrs={
                'class' : STYLE_DE_BASE, 
                'placeholder' : 'quantite'
            }),
            }