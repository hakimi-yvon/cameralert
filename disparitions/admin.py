from django.contrib import admin
from .models import PersonneDisparue


def valider_cas(modeladmin, request, queryset):
    queryset.update(statut='en_recherche')
    modeladmin.message_user(
        request, 
        f"{queryset.count()} cas validé(s) et publié(s) avec succès."
    )
valider_cas.short_description = "Valider et publier les cas sélectionnés"

@admin.register(PersonneDisparue)
class PersonneDisparueAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste
    list_display = [
        'reference',
        'nom', 
        'prenom', 
        'age',
        'region', 
        'date_disparition',
        'statut',
        'date_creation'
    ]
    
    actions = ['valider_cas']

    # Filtres sur le côté droit
    list_filter = [
        'statut', 
        'region', 
        'categorie', 
        'sexe'
    ]

    # Barre de recherche
    search_fields = [
        'nom', 
        'prenom', 
        'region', 
        'ville'
    ]

    # Champs non modifiables
    readonly_fields = [
        'reference',
        'date_creation', 
        'date_modification'
    ]

    # Grouper les champs par section
    fieldsets = [
        ('Identité', {
            'fields': [
                'reference',
                'nom', 
                'prenom', 
                'age', 
                'sexe',
                'categorie',
                'photo'
            ]
        }),
        ('Description physique', {
            'fields': [
                'taille', 
                'teint', 
                'signes_particuliers'
            ]
        }),
        ('Circonstances', {
            'fields': [
                'date_disparition',
                'heure_disparition',
                'region',
                'ville',
                'vetements',
                'description'
            ]
        }),
        ('Statut', {
            'fields': [
                'statut', 
                'declarant'
            ]
        }),
        ('Dates', {
            'fields': [
                'date_creation', 
                'date_modification'
            ]
        }),
    ]