from django import forms
from .models import Adherent

class FormulaireAjoutAdherent(forms.ModelForm):
    class Meta:
        model = Adherent
        fields = '__all__'
        widgets = {
            'matricule' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'nom' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'prenom' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'email' : forms.EmailInput(attrs={
                'class' : 'form-control'
            }),
            'fonctions' : forms.Select(attrs={
                'class' : 'form-control'
            })
        }