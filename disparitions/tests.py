from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import PersonneDisparue
from .forms import PersonneDisparueForm


class PersonneDisparueModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='declarant1', password='Password123!')

    def test_creation_personne_disparue_et_reference_automatique(self):
        """Vérifie que la référence est automatiquement générée au format CA-YYYY-XXXX."""
        cas = PersonneDisparue.objects.create(
            nom='Mbarga',
            prenom='Emmanuel',
            age=25,
            sexe='garcon_homme',
            categorie='homme',
            date_disparition=date.today() - timedelta(days=2),
            region='Centre',
            ville='Yaoundé',
            telephone_contact='+237699112233',
            description='Disparu au quartier Bastos.',
            declarant=self.user
        )
        annee = date.today().year
        self.assertTrue(cas.reference.startswith(f"CA-{annee}-"))
        self.assertEqual(cas.statut, 'en_attente')
        self.assertEqual(cas.telephone_contact_wa, '237699112233')

    def test_validation_formulaire_date_future_interdite(self):
        """Vérifie qu'un signalement avec date de disparition future est rejeté."""
        data = {
            'nom': 'Kamga',
            'prenom': 'Jean',
            'age': 30,
            'sexe': 'garcon_homme',
            'categorie': 'homme',
            'date_disparition': date.today() + timedelta(days=5),
            'region': 'Littoral',
            'ville': 'Douala',
            'telephone_contact': '677001122',
            'description': 'Description du cas',
        }
        form = PersonneDisparueForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_disparition', form.errors)


class PersonneDisparueViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='Password123!', email='user1@test.com')
        self.staff_user = User.objects.create_user(username='admin1', password='Password123!', is_staff=True)

        self.cas_valide = PersonneDisparue.objects.create(
            nom='Fotso',
            prenom='Alain',
            age=18,
            sexe='garcon_homme',
            categorie='homme',
            date_disparition=date.today() - timedelta(days=1),
            region='Ouest',
            ville='Bafoussam',
            description='Vu pour la dernière fois au marché.',
            statut='en_recherche',
            declarant=self.user
        )

        self.cas_en_attente = PersonneDisparue.objects.create(
            nom='Ngo',
            prenom='Marie',
            age=14,
            sexe='fille_femme',
            categorie='enfant',
            date_disparition=date.today() - timedelta(days=3),
            region='Littoral',
            ville='Douala',
            description='Disparue en rentrant de l\'école.',
            statut='en_attente',
            declarant=self.user
        )

    def test_page_accueil_charge_avec_succes(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fotso')
        self.assertNotContains(response, 'Ngo')  # Le cas en attente ne doit pas s'afficher

    def test_liste_cas_avec_filtres(self):
        response = self.client.get(reverse('liste_cas') + '?region=Ouest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fotso')

    def test_detail_cas_et_affiche_a4(self):
        response = self.client.get(reverse('detail_cas', args=[self.cas_valide.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fotso')

        response_affiche = self.client.get(reverse('affiche_cas', args=[self.cas_valide.pk]))
        self.assertEqual(response_affiche.status_code, 200)
        self.assertContains(response_affiche, 'Avis de Recherche')

    def test_marquer_retrouve_requiert_post(self):
        """Vérifie que la clôture d'un cas rejette les requêtes GET (CSRF protection)."""
        self.client.login(username='user1', password='Password123!')
        url = reverse('marquer_retrouve', args=[self.cas_valide.pk])

        # En GET, doit être rejeté (HTTP 405 Method Not Allowed)
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 405)

        # En POST, doit fonctionner
        response_post = self.client.post(url)
        self.assertEqual(response_post.status_code, 302)
        self.cas_valide.refresh_from_db()
        self.assertEqual(self.cas_valide.statut, 'retrouvee')

    def test_validation_cas_par_staff_uniquement(self):
        """Vérifie que seul un modérateur peut valider un cas et en POST."""
        url = reverse('valider_cas', args=[self.cas_en_attente.pk])

        # Utilisateur normal -> refusé / redirigé vers login staff
        self.client.login(username='user1', password='Password123!')
        response = self.client.post(url)
        self.assertNotEqual(self.cas_en_attente.statut, 'en_recherche')

        # Utilisateur staff -> accepté en POST
        self.client.login(username='admin1', password='Password123!')
        response_staff = self.client.post(url)
        self.assertEqual(response_staff.status_code, 302)
        self.cas_en_attente.refresh_from_db()
        self.assertEqual(self.cas_en_attente.statut, 'en_recherche')

    def test_mes_signalements_page(self):
        url = reverse('mes_signalements')
        # Anonyme redirigé vers connexion
        response_anon = self.client.get(url)
        self.assertEqual(response_anon.status_code, 302)

        # Connecté -> voit ses deux signalements
        self.client.login(username='user1', password='Password123!')
        response_auth = self.client.get(url)
        self.assertEqual(response_auth.status_code, 200)
        self.assertContains(response_auth, 'Fotso')
        self.assertContains(response_auth, 'Ngo')
