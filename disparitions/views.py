from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count
import json
from .models import PersonneDisparue
from .forms import PersonneDisparueForm
from .emails import envoyer_email_validation, envoyer_email_rejet, envoyer_email_retrouve
from django.core.paginator import Paginator

def accueil(request):
    # Les 6 derniers cas en recherche
    cas_recents = PersonneDisparue.objects.filter(
        statut='en_recherche'
    )[:6]

    # Statistiques
    total_actifs = PersonneDisparue.objects.filter(
        statut='en_recherche'
    ).count()
    total_retrouves = PersonneDisparue.objects.filter(
        statut='retrouvee'
    ).count()

    return render(request, 'disparitions/accueil.html', {
        'cas_recents': cas_recents,
        'total_actifs': total_actifs,
        'total_retrouves': total_retrouves,
    })

def liste_cas(request):
    cas = PersonneDisparue.objects.filter(statut='en_recherche')

    # Recherche par nom
    recherche = request.GET.get('q')
    if recherche:
        cas = cas.filter(nom__icontains=recherche) | \
              cas.filter(prenom__icontains=recherche)

    # Filtre par région
    region = request.GET.get('region')
    if region:
        cas = cas.filter(region=region)

    # Filtre par catégorie
    categorie = request.GET.get('categorie')
    if categorie:
        cas = cas.filter(categorie=categorie)

    # Filtre par ancienneté de la disparition
    from datetime import date, timedelta
    anciennete = request.GET.get('anciennete')
    if anciennete == 'moins_30':
        seuil = date.today() - timedelta(days=30)
        cas = cas.filter(date_disparition__gte=seuil)
    elif anciennete == 'plus_30':
        seuil = date.today() - timedelta(days=30)
        cas = cas.filter(date_disparition__lt=seuil)
    elif anciennete == 'plus_90':
        seuil = date.today() - timedelta(days=90)
        cas = cas.filter(date_disparition__lt=seuil)

    # Tri
    tri = request.GET.get('tri', 'recent')
    if tri == 'ancien':
        cas = cas.order_by('date_disparition')
    else:
        cas = cas.order_by('-date_disparition')

    # Pagination — 12 cas par page
    paginator = Paginator(cas, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'disparitions/liste_cas.html', {
        'cas': page_obj,
        'recherche': recherche,
        'region': region,
        'categorie': categorie,
        'tri': tri,
        'anciennete': anciennete,
        'page_obj': page_obj,
    })

def detail_cas(request, pk):
    cas = get_object_or_404(PersonneDisparue, pk=pk)
    temoignages = cas.temoignages.filter(est_valide=True)

    return render(request, 'disparitions/detail_cas.html', {
        'cas': cas,
        'temoignages': temoignages,
    })

def affiche_cas(request, pk):
    """Affiche A4 imprimable et partageable haute définition avec QR Code."""
    cas = get_object_or_404(PersonneDisparue, pk=pk)
    url_fiche = request.build_absolute_uri(f'/cas/{cas.pk}/')
    return render(request, 'disparitions/affiche_cas.html', {
        'cas': cas,
        'url_fiche': url_fiche,
    })

@login_required
def mes_signalements(request):
    """Espace personnel listant les signalements déposés par l'utilisateur connecté."""
    cas_list = PersonneDisparue.objects.filter(declarant=request.user).order_by('-date_creation')
    return render(request, 'disparitions/mes_signalements.html', {
        'cas_list': cas_list
    })

@login_required
def signaler(request):
    if request.method == 'POST':
        form = PersonneDisparueForm(request.POST, request.FILES)
        if form.is_valid():
            cas = form.save(commit=False)
            cas.declarant = request.user
            cas.save()
            messages.success(
                request, 
                'Votre signalement a été soumis avec succès. '
                'Il sera publié après validation par notre équipe.'
            )
            return redirect('accueil')
    else:
        form = PersonneDisparueForm()

    return render(request, 'disparitions/signaler.html', {
        'form': form
    })

def carte_disparitions(request):
    """Vue de la carte interactive des disparitions par région."""

    # Coordonnées GPS des 10 régions du Cameroun
    COORDS_REGIONS = {
        'Centre':       {'lat': 4.3612,  'lng': 11.5197},
        'Littoral':     {'lat': 4.0511,  'lng': 9.7679},
        'Nord':         {'lat': 9.3044,  'lng': 13.3952},
        'Extreme Nord': {'lat': 10.5957, 'lng': 14.3300},
        'Ouest':        {'lat': 5.4767,  'lng': 10.4214},
        'Sud':          {'lat': 3.0667,  'lng': 11.8667},
        'Est':          {'lat': 4.6050,  'lng': 13.6826},
        'Adamaoua':     {'lat': 7.3304,  'lng': 13.5783},
        'Nord Ouest':   {'lat': 6.3127,  'lng': 10.2613},
        'Sud Ouest':    {'lat': 4.5561,  'lng': 9.3547},
    }

    # Agréger les cas actifs par région
    regions_data = PersonneDisparue.objects.filter(
        statut='en_recherche'
    ).values('region').annotate(total=Count('id'))

    # Construire la liste pour Leaflet
    markers = []
    for item in regions_data:
        nom_region = item['region']
        coords = COORDS_REGIONS.get(nom_region)
        if coords:
            markers.append({
                'region': nom_region,
                'total': item['total'],
                'lat': coords['lat'],
                'lng': coords['lng'],
            })

    total_actifs = PersonneDisparue.objects.filter(statut='en_recherche').count()
    total_retrouves = PersonneDisparue.objects.filter(statut='retrouvee').count()

    return render(request, 'disparitions/carte.html', {
        'markers_json': json.dumps(markers),
        'total_actifs': total_actifs,
        'total_retrouves': total_retrouves,
    })

from django.views.decorators.http import require_POST

@login_required
@require_POST
def marquer_retrouve(request, pk):
    cas = get_object_or_404(PersonneDisparue, pk=pk)
    
    # Seul l'administrateur ou le déclarant original peut marquer le cas comme retrouvé
    if not (request.user.is_staff or cas.declarant == request.user):
        messages.error(request, "Vous n'avez pas l'autorisation de modifier ce signalement.")
        return redirect('detail_cas', pk=pk)

    cas.statut = 'retrouvee'
    cas.save()
    envoyer_email_retrouve(cas, request)
    messages.success(request, f'{cas.prenom} {cas.nom} a été marqué(e) comme retrouvé(e).')
    return redirect('detail_cas', pk=pk)

@staff_member_required
@require_POST
def valider_cas(request, pk):
    cas = get_object_or_404(PersonneDisparue, pk=pk)
    cas.statut = 'en_recherche'
    cas.save()
    envoyer_email_validation(cas, request)
    messages.success(
        request,
        f'Le cas de {cas.prenom} {cas.nom} a été validé et publié.'
    )
    return redirect('dashboard')

@staff_member_required
@require_POST
def rejeter_cas(request, pk):
    cas = get_object_or_404(PersonneDisparue, pk=pk)
    cas.statut = 'rejete'
    cas.save()
    envoyer_email_rejet(cas, request)
    messages.warning(
        request,
        f'Le cas de {cas.prenom} {cas.nom} a été rejeté.'
    )
    return redirect('dashboard')