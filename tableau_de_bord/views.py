from django.shortcuts import render

def index_dashboard(request):
    return render(request, 'tableau_de_bord/index.html')


