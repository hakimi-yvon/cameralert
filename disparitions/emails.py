"""
Fonctions d'envoi d'emails pour CamerAlert.
Utilisées lors des changements de statut d'un cas de disparition.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def _get_declarant_email(cas):
    """Retourne l'email du déclarant si disponible."""
    if cas.declarant and cas.declarant.email:
        return cas.declarant.email
    return None


def envoyer_email_validation(cas, request):
    """Email envoyé au déclarant quand son signalement est validé et publié."""
    destinataire = _get_declarant_email(cas)
    if not destinataire:
        return

    url_cas = request.build_absolute_uri(f'/cas/{cas.pk}/')

    contexte = {
        'cas': cas,
        'url_cas': url_cas,
        'prenom_declarant': cas.declarant.first_name or cas.declarant.username,
    }

    sujet = f"[CamerAlert] Votre signalement a été validé — {cas.prenom} {cas.nom}"
    html_message = render_to_string('emails/validation.html', contexte)
    message_texte = strip_tags(html_message)

    try:
        send_mail(
            subject=sujet,
            message=message_texte,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinataire],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception:
        pass  # Ne jamais bloquer le flux principal à cause d'un email


def envoyer_email_rejet(cas, request):
    """Email envoyé au déclarant quand son signalement est rejeté."""
    destinataire = _get_declarant_email(cas)
    if not destinataire:
        return

    contexte = {
        'cas': cas,
        'prenom_declarant': cas.declarant.first_name or cas.declarant.username,
    }

    sujet = f"[CamerAlert] Mise à jour de votre signalement — {cas.prenom} {cas.nom}"
    html_message = render_to_string('emails/rejet.html', contexte)
    message_texte = strip_tags(html_message)

    try:
        send_mail(
            subject=sujet,
            message=message_texte,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinataire],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception:
        pass


def envoyer_email_retrouve(cas, request):
    """Email envoyé au déclarant quand la personne est retrouvée."""
    destinataire = _get_declarant_email(cas)
    if not destinataire:
        return

    url_cas = request.build_absolute_uri(f'/cas/{cas.pk}/')

    contexte = {
        'cas': cas,
        'url_cas': url_cas,
        'prenom_declarant': cas.declarant.first_name or cas.declarant.username,
    }

    sujet = f"[CamerAlert] Bonne nouvelle — {cas.prenom} {cas.nom} a été retrouvé(e) !"
    html_message = render_to_string('emails/retrouve.html', contexte)
    message_texte = strip_tags(html_message)

    try:
        send_mail(
            subject=sujet,
            message=message_texte,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinataire],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception:
        pass
