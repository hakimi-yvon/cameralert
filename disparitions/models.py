from django.db import models
from django.contrib.auth.models import User

class PersonneDisparue(models.Model):

    # Choix possibles pour le statut
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('en_recherche', 'En recherche'),
        ('retrouvee', 'Retrouvée'),
        ('rejete', 'Rejeté'),
    ]

    # Choix possibles pour le sexe
    SEXE_CHOICES = [
        ('fille_femme', 'Fille / Femme'),
        ('garcon_homme', 'Garçon / Homme'),
    ]

    # Choix possibles pour la catégorie
    CATEGORIE_CHOICES = [
        ('enfant', 'Enfant'),
        ('femme', 'Femme'),
        ('homme', 'Homme'),
        ('personne_agee', 'Personne âgée'),
    ]

    # Choix possibles pour la région
    REGION_CHOICES = [
        ('Adamaoua', 'Adamaoua'),
        ('Centre', 'Centre'),
        ('Est', 'Est'),
        ('Extreme Nord', 'Extrême-Nord'),
        ('Littoral', 'Littoral'),
        ('Nord', 'Nord'),
        ('Nord Ouest', 'Nord-Ouest'),
        ('Ouest', 'Ouest'),
        ('Sud', 'Sud'),
        ('Sud Ouest', 'Sud-Ouest'),
    ]

    # Informations de base
    reference = models.CharField(max_length=20, unique=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sexe = models.CharField(max_length=20, choices=SEXE_CHOICES)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)

    # Description physique
    taille = models.CharField(max_length=20, blank=True)
    teint = models.CharField(max_length=50, blank=True)
    signes_particuliers = models.TextField(blank=True)

    # Circonstances
    date_disparition = models.DateField()
    heure_disparition = models.TimeField(null=True, blank=True)
    region = models.CharField(max_length=100, choices=REGION_CHOICES)
    ville = models.CharField(max_length=100)
    vetements = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    # Photo
    photo = models.ImageField(
        upload_to='disparitions/', 
        null=True, 
        blank=True
    )

    # Statut du cas
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    # Qui a fait le signalement
    declarant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='signalements'
    )

    # Dates automatiques
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Si la fiche est nouvelle et n'a pas encore de référence
        if not self.reference:
            from datetime import date
            from django.db.models import Max
            import re

            annee = date.today().year
            prefix = f"CA-{annee}-"

            # Trouver le numéro le plus élevé déjà utilisé cette année
            existants = PersonneDisparue.objects.filter(
                reference__startswith=prefix
            ).values_list('reference', flat=True)

            max_num = 0
            for ref in existants:
                try:
                    num = int(ref[len(prefix):])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass

            # On génère la référence : CA-2026-0001
            self.reference = f"{prefix}{max_num + 1:04d}"

        # On sauvegarde normalement
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.region}"

    class Meta:
        verbose_name = "Personne disparue"
        verbose_name_plural = "Personnes disparues"
        ordering = ['-date_creation']