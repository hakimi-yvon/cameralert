from django.contrib import admin
from .models import Temoignage

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste
    list_display = [
        'personne',
        'auteur_nom',
        'auteur_telephone',
        'lieu',
        'date_observation',
        'est_valide',
        'date_soumission'
    ]

    # Filtres sur le côté droit
    list_filter = [
        'est_valide',
        'date_soumission'
    ]

    # Barre de recherche
    search_fields = [
        'auteur_nom',
        'auteur_telephone',
        'lieu',
        'message'
    ]

    # Champs non modifiables
    readonly_fields = ['date_soumission']