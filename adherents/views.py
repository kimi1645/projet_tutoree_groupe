from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Adherent
from .forms import FormulaireAjoutAdherent

def liste_adherents(request):
    adherents = Adherent.objects.all()
    return render(request, "adherent/liste_adherent.html", 
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
        return render(request, "adherent/ajouter.html", {
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
        return render(request, "adherent/modifier.html", {
            'form' : form
        })