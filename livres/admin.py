from django.contrib import admin
from .models import Livre
import re
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin


class LivreRessource(resources.ModelResource):
    class Meta:
        model = Livre
        import_id_fields = ('reference',)
        fields = ('reference', 'titre', 'auteur', 'categorie', 'quantite')


@admin.register(Livre)
class LivreAdmin(ImportExportModelAdmin):
    resource_class = LivreRessource