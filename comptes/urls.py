from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # Réinitialisation de mot de passe
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(
        template_name='comptes/password_reset_form.html',
        email_template_name='comptes/password_reset_email.html',
        subject_template_name='comptes/password_reset_subject.txt',
    ), name='password_reset'),
    path('mot-de-passe-oublie/envoye/', auth_views.PasswordResetDoneView.as_view(
        template_name='comptes/password_reset_done.html',
    ), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='comptes/password_reset_confirm.html',
    ), name='password_reset_confirm'),
    path('reinitialiser/termine/', auth_views.PasswordResetCompleteView.as_view(
        template_name='comptes/password_reset_complete.html',
    ), name='password_reset_complete'),
]