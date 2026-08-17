from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from disparitions.models import PersonneDisparue
from temoignages.models import Temoignage
from django.contrib.auth.models import User

@staff_member_required
def tableau_de_bord(request):

    # Statistiques principales
    total_actifs = PersonneDisparue.objects.filter(
        statut='en_recherche'
    ).count()

    en_attente = PersonneDisparue.objects.filter(
        statut='en_attente'
    ).count()

    total_retrouves = PersonneDisparue.objects.filter(
        statut='retrouvee'
    ).count()

    total_temoignages = Temoignage.objects.count()

    # Cas en attente de modération
    cas_en_attente = PersonneDisparue.objects.filter(
        statut='en_attente'
    ).order_by('-date_creation')

    # Témoignages en attente de modération
    temoignages_en_attente = Temoignage.objects.filter(
        est_valide=False
    ).select_related('personne').order_by('-date_soumission')

    # Activité récente (dernières 24h)
    hier = timezone.now() - timedelta(hours=24)

    temoignages_recents = Temoignage.objects.filter(
        date_soumission__gte=hier
    ).select_related('personne').order_by('-date_soumission')[:5]

    cas_recents_valides = PersonneDisparue.objects.filter(
        date_creation__gte=hier
    ).order_by('-date_creation')[:5]

    cas_retrouves_recents = PersonneDisparue.objects.filter(
        statut='retrouvee',
        date_modification__gte=hier
    ).order_by('-date_modification')[:3]

    # Cas par région
    from django.db.models import Count
    regions = PersonneDisparue.objects.filter(
        statut='en_recherche'
    ).values('region').annotate(
        total=Count('id')
    ).order_by('-total')[:6]

    # Calcul du max pour les barres de progression
    max_region = regions[0]['total'] if regions else 1

    return render(request, 'dashboard/tableau_de_bord.html', {
        'total_actifs': total_actifs,
        'en_attente': en_attente,
        'total_retrouves': total_retrouves,
        'total_temoignages': total_temoignages,
        'cas_en_attente': cas_en_attente,
        'temoignages_en_attente': temoignages_en_attente,
        'temoignages_recents': temoignages_recents,
        'cas_recents_valides': cas_recents_valides,
        'cas_retrouves_recents': cas_retrouves_recents,
        'regions': regions,
        'max_region': max_region,
    })