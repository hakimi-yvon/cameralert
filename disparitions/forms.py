from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import PersonneDisparue

class PersonneDisparueForm(forms.ModelForm):
    class Meta:
        model = PersonneDisparue
        fields = [
            'nom', 'prenom', 'age', 'sexe', 'categorie',
            'taille', 'teint', 'signes_particuliers',
            'date_disparition', 'heure_disparition',
            'region', 'ville', 'vetements',
            'telephone_contact',
            'description', 'photo',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Ex: Kamga, Mbarga, Aboubakar...'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Ex: Christian, Aminatou...'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Ex: 15', 'min': 0, 'max': 120}),
            'taille': forms.TextInput(attrs={'placeholder': 'Ex: 1m65, 1m75...'}),
            'teint': forms.TextInput(attrs={'placeholder': 'Ex: Ébène, Clair, Noir, Métis...'}),
            'signes_particuliers': forms.TextInput(attrs={'placeholder': 'Ex: Cicatrice au front, lunettes de vue, grain de beauté...'}),
            'vetements': forms.TextInput(attrs={'placeholder': 'Ex: Polo rouge, pantalon noir, baskets blanches...'}),
            'date_disparition': forms.DateInput(attrs={'type': 'date'}),
            'heure_disparition': forms.TimeInput(attrs={'type': 'time'}),
            'ville': forms.TextInput(attrs={'placeholder': 'Ex: Douala (Akwa), Yaoundé (Bastos), Bafoussam...'}),
            'telephone_contact': forms.TextInput(
                attrs={'placeholder': 'Ex: +237 690 00 00 00 (Orange, MTN, WhatsApp)'}
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Expliquez précisément le déroulement : dernier endroit où la personne a été aperçue, direction prise, état de santé (Alzheimer, épilepsie...), toute information utile pour les recherches.'
                }
            ),
        }

    def clean_date_disparition(self):
        date_disparition = self.cleaned_data.get('date_disparition')
        if date_disparition and date_disparition > date.today():
            raise ValidationError("La date de disparition ne peut pas être située dans le futur.")
        return date_disparition

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and hasattr(photo, 'size'):
            max_size_mb = 5
            if photo.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"La taille de l'image ne doit pas dépasser {max_size_mb} Mo.")
        return photo