from django import forms
from .models import Temoignage

class TemoignageForm(forms.ModelForm):
    class Meta:
        model = Temoignage
        fields = [
            'auteur_nom',
            'auteur_telephone',
            'lieu',
            'date_observation',
            'message',
        ]
        labels = {
            'auteur_nom': 'Votre nom ou pseudonyme (optionnel)',
            'auteur_telephone': 'Votre numéro de téléphone (confidentiel)',
            'lieu': 'Lieu précis où vous avez vu la personne',
            'date_observation': "Date de l'observation",
            'message': 'Description détaillée de votre observation',
        }
        widgets = {
            'auteur_nom': forms.TextInput(
                attrs={'placeholder': 'Ex: Jean M. ou Laisser vide'}
            ),
            'auteur_telephone': forms.TextInput(
                attrs={'placeholder': 'Ex: +237 6XX XX XX XX (joignable en cas de précision)'}
            ),
            'lieu': forms.TextInput(
                attrs={'placeholder': 'Ex: Douala, Carrefour Ndokoti, près de la station'}
            ),
            'date_observation': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'message': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Décrivez précisément ce que vous avez observé : l’état de la personne, la direction prise, si elle était seule ou accompagnée, ses vêtements...'
                }
            ),
        }