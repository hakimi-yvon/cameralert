from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from disparitions.models import PersonneDisparue
from .models import Temoignage


class TemoignagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(username='modo', password='Password123!', is_staff=True)
        self.cas = PersonneDisparue.objects.create(
            nom='Biloa',
            prenom='Grace',
            age=16,
            sexe='fille_femme',
            categorie='enfant',
            date_disparition=date.today(),
            region='Centre',
            ville='Yaoundé',
            description='Enfant portée disparue.',
            statut='en_recherche'
        )

    def test_soumission_temoignage(self):
        """Vérifie la soumission d'un témoignage et son statut non validé par défaut."""
        data = {
            'auteur_nom': 'Jean Marc',
            'auteur_telephone': '+237699999999',
            'lieu': 'Carrefour Emia, Yaoundé',
            'date_observation': date.today(),
            'message': 'Je crois avoir vu une jeune fille correspondant au signalement ce matin.',
        }
        response = self.client.post(reverse('soumettre_temoignage', args=[self.cas.pk]), data=data)
        self.assertEqual(response.status_code, 302)

        temoignage = Temoignage.objects.filter(personne=self.cas).first()
        self.assertIsNotNone(temoignage)
        self.assertFalse(temoignage.est_valide)

    def test_moderation_temoignage_validation_et_suppression(self):
        """Vérifie que la validation et la suppression d'un témoignage exigent POST et staff."""
        temoignage = Temoignage.objects.create(
            personne=self.cas,
            auteur_nom='Témoin 1',
            auteur_telephone='670000000',
            lieu='Douala',
            date_observation=date.today(),
            message='Aperçue à Bonanjo.'
        )

        valider_url = reverse('valider_temoignage', args=[temoignage.pk])
        supprimer_url = reverse('supprimer_temoignage', args=[temoignage.pk])

        # Tentative GET -> 405 Method Not Allowed
        self.client.login(username='modo', password='Password123!')
        response_get = self.client.get(valider_url)
        self.assertEqual(response_get.status_code, 405)

        # Validation en POST
        response_post = self.client.post(valider_url)
        self.assertEqual(response_post.status_code, 302)
        temoignage.refresh_from_db()
        self.assertTrue(temoignage.est_valide)

        # Suppression en POST
        response_del = self.client.post(supprimer_url)
        self.assertEqual(response_del.status_code, 302)
        self.assertFalse(Temoignage.objects.filter(pk=temoignage.pk).exists())
