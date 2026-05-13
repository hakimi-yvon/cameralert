from django.db import models
from disparitions.models import PersonneDisparue

class Temoignage(models.Model):

    # La personne concernée par ce témoignage
    personne = models.ForeignKey(
        PersonneDisparue,
        on_delete=models.CASCADE,
        related_name='temoignages'
    )

    # Informations sur la personne qui témoigne
    auteur_nom = models.CharField(max_length=100, blank=True)
    auteur_telephone = models.CharField(max_length=20)

    # Contenu du témoignage
    lieu = models.CharField(max_length=200)
    date_observation = models.DateField()
    message = models.TextField()

    # Validation par l'admin
    est_valide = models.BooleanField(default=False)

    # Date automatique
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Témoignage sur {self.personne} - {self.date_soumission}"

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-date_soumission']