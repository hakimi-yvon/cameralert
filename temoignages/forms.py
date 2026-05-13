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
        widgets = {
            'date_observation': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'message': forms.Textarea(
                attrs={'rows': 4}
            ),
        }