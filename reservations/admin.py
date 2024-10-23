from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Billet

class BilletAdmin(admin.ModelAdmin):
    list_display = ('type_billet', 'prix', 'disponible', 'date_concert', 'nombre_disponible')  # Colonnes affichées dans l'admin
    list_filter = ('type_billet', 'disponible')  # Filtres dans la barre latérale
    search_fields = ('type_billet',)  # Recherche par type de billet

admin.site.register(Billet, BilletAdmin)
