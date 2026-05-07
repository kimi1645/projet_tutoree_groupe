from django import forms
from .models import Emprunt


#class EmpruntForm(forms.ModelForm):
#    class Meta :
#        model = Emprunt
#        fields= ['ref_livre','adherent']
#        widgets = {
#            'ref_livre' : forms.Select(attrs={
#                'class' : 'form-control'
#            }),
#            'adherent' : forms.Select(attrs={
#                'class' : 'form-control'
#            })
#        }


class EnregistrementRetourEmprunt(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['date_retour','remarque']
        widgets = {
            'date_retour' : forms.DateInput(attrs={
                'class' : 'form-control datepicker',
                'type' :'date',
                'id' : 'date_retour',
                'readonly' : True
            }),
            'remarque' : forms.Textarea(attrs={
                'class' : 'form-control'
            })
        }