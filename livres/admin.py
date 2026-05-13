from django.contrib import admin
from .models import Livre
import re
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin


class LivreRessource(resources.ModelResource):
    class Meta:
        model = Livre
        fields = '__all__'


    # Méthode pour corriger les données avant insertion
    def before_import_row(self, row, **kwargs):
        titre_sale=row.get('titre')
        if titre_sale:
            titre_propre = re.sub(r'([a-z])([A-Z])', r'\1 \2', titre_sale)
            row['titre'] = titre_propre

@admin.register(Livre)
class LivreAdmin(ImportExportModelAdmin):
    resource_classe = LivreRessource