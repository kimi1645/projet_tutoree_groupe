from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Adherent, CompteAdherent
from .forms import FormulaireAjoutAdherent, FormulaireInscription, VerificationParEmail, FormulaireReservation, DetailReservationFormSet, DetailReservationInlineFormSet
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.conf import settings

def liste_adherents(request):
    adherents = Adherent.objects.all()
    return render(request, "adherents/liste_adherent.html", 
                  {'adherents' : adherents})

def ajouter_adherent(request):
    if request.method == "POST":
        form = FormulaireAjoutAdherent(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeAdherent')
        else:
            return HttpResponse("Vérifiez bien vos données")
    else:
        form = FormulaireAjoutAdherent()
        return render(request, "adherents/ajouter.html", {
            'form' : form
        })
    

def modifier_adherent(request, id):
    adherent = get_object_or_404(Adherent, pk=id)
    if request.method == "POST":
        form = FormulaireAjoutAdherent(request.POST, instance=adherent)
        if form.is_valid():
            form.save()
            return redirect('listeAdherent')
        else:
            return HttpResponse("Modification non valide")
    else:
        form = FormulaireAjoutAdherent(instance=adherent)
        return render(request, "adherents/modifier.html", {
            'form' : form
        })


def verification(request):
    if request.method == "POST":
        form = VerificationParEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = ''
            for c in random.sample(range(1,9), 5):
                otp += str(c)
            request.session['otp_code'] = otp
            request.session['otp_email'] = email
            send_mail(
                subject='Rappel- Retour de livre',
                message=f'Bonjour voici votre code OTP {otp}',
                from_email='stockalerte85@gmail.com',
                recipient_list=[email]
            )
            return redirect('inscription')
    else:
        form = VerificationParEmail()
    return render(request, 'adherents/verification.html', {
        'form' : form
    })


# views.py
def inscription(request):
    otp_attendu = request.session.get('otp_code')
    email_verifie = request.session.get('otp_email')

    if not otp_attendu:
        return redirect('verification')
    
    if request.method == 'POST':
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            
            otp_saisi = form.cleaned_data['code_otp']
            if otp_saisi == otp_attendu:
                matricule = form.cleaned_data['matricule']
                username  = form.cleaned_data['username']
                password  = form.cleaned_data['password']
                #Recuperer le personneautoriséé (adherent)
                personne = Adherent.objects.get(matricule=matricule)

                #Création d'un utilisateur django associé
                user = User.objects.create_user(
                    username = username,
                    password = password,
                    email    = personne.email,
                )

                # Création de la compte pour l'adherent
                CompteAdherent.objects.create(
                    user     = user,
                    personne = personne,
                )
                return redirect('seConnecter')
            else:
                form.add_error('otp', 'Le code OTP est incorrect')
            
    else:

        form = FormulaireInscription()

    return render(request, 'adherents/inscription.html', {'form': form})



#Views qui gère la réservation
def reservation_avec_detail(request):
    if request.method == "POST":
        reservation_form = FormulaireReservation(request.POST)
       
        #Vérifiation si la formulaire est ok
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            #Recuperer l'adhérent connecté
            adherent = request.user.compteadherent.personne
            reservation.adherent = adherent
            detail_reservation_form = DetailReservationInlineFormSet(request.POST, instance=reservation)
            if detail_reservation_form.is_valid():
                #Enregistrement après validation
                reservation.save()
                detail_reservation_form.save()

                return HttpResponse("Reservation effectué avec succès")
            
    else:
        reservation_form = FormulaireReservation()
        detail_reservation_form = DetailReservationInlineFormSet()
        
    context = {
        'reservation_form' : reservation_form,
        'detail_reservation_form' : detail_reservation_form
    }
    return render(request, 'adherents/reservation.html', context)    