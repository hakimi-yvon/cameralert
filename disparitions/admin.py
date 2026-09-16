from django.contrib import admin
from .models import PersonneDisparue


from .emails import envoyer_email_validation

def valider_cas(modeladmin, request, queryset):
    count = 0
    for cas in queryset:
        cas.statut = 'en_recherche'
        cas.save()
        envoyer_email_validation(cas, request)
        count += 1
    modeladmin.message_user(
        request, 
        f"{count} cas validé(s) et publié(s) avec succès (avec notification email aux déclarants)."
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
        'telephone_contact',
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
        'ville',
        'telephone_contact'
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
        ('Circonstances & Contact', {
            'fields': [
                'date_disparition',
                'heure_disparition',
                'region',
                'ville',
                'telephone_contact',
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