from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class ComptesViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_inscription_utilisateur(self):
        """Vérifie la création de compte et la connexion automatique."""
        data = {
            'first_name': 'Paul',
            'last_name': 'Biya',
            'username': 'paul_test',
            'email': 'paul@example.cm',
            'password1': 'StrongSecret2026!',
            'password2': 'StrongSecret2026!',
        }
        response = self.client.post(reverse('inscription'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='paul_test').exists())

    def test_connexion_et_deconnexion(self):
        """Vérifie l'authentification et la déconnexion."""
        User.objects.create_user(username='testeur', password='Password123!')

        # Connexion valide
        response_login = self.client.post(reverse('connexion'), {
            'username': 'testeur',
            'password': 'Password123!',
        })
        self.assertEqual(response_login.status_code, 302)

        # Déconnexion
        response_logout = self.client.post(reverse('deconnexion'))
        self.assertEqual(response_logout.status_code, 302)

    def test_page_mot_de_passe_oublie_accessible(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mot de passe oublié ?')
