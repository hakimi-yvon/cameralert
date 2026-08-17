from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class InscriptionForm(UserCreationForm):

    # Champs supplémentaires
    email = forms.EmailField(
        required=True,
        label="Adresse email (nécessaire pour les notifications)",
        help_text="Vous recevrez les alertes et le suivi de vos signalements."
    )
    first_name = forms.CharField(
        max_length=100,
        label="Prénom",
        required=True
    )
    last_name = forms.CharField(
        max_length=100,
        label="Nom",
        required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name', 
            'username',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traduire les labels en français
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"
        self.fields['username'].help_text = "150 caractères max. Lettres, chiffres et @/./+/-/_ uniquement."
        self.fields['password1'].help_text = "Au moins 8 caractères."
        self.fields['password2'].help_text = "Entrez le même mot de passe pour confirmation."