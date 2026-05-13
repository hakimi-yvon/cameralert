from django import forms
from .models import PersonneDisparue

class PersonneDisparueForm(forms.ModelForm):
    class Meta:
        model = PersonneDisparue
        fields = [
            'nom', 'prenom', 'age', 'sexe', 'categorie',
            'taille', 'teint', 'signes_particuliers',
            'date_disparition', 'heure_disparition',
            'region', 'ville', 'vetements',
            'description', 'photo',
        ]
        widgets = {
            'date_disparition': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'heure_disparition': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4}
            ),
        }