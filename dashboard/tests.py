from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from disparitions.models import PersonneDisparue


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='simple_user', password='Password123!')
        self.admin = User.objects.create_user(username='super_admin', password='Password123!', is_staff=True)

        PersonneDisparue.objects.create(
            nom='Onana',
            prenom='André',
            age=27,
            sexe='garcon_homme',
            categorie='homme',
            date_disparition=date.today(),
            region='Centre',
            ville='Yaoundé',
            description='En attente',
            statut='en_attente'
        )

    def test_acces_dashboard_restreint_au_staff(self):
        url = reverse('dashboard')

        # Non connecté -> redirigé vers login admin
        response_anon = self.client.get(url)
        self.assertEqual(response_anon.status_code, 302)

        # Utilisateur normal -> redirigé
        self.client.login(username='simple_user', password='Password123!')
        response_user = self.client.get(url)
        self.assertEqual(response_user.status_code, 302)

        # Admin / Staff -> Accès autorisé (200)
        self.client.login(username='super_admin', password='Password123!')
        response_admin = self.client.get(url)
        self.assertEqual(response_admin.status_code, 200)
        self.assertContains(response_admin, 'Onana')
        self.assertContains(response_admin, 'Tableau de bord')
