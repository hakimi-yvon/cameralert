from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.accueil, name='accueil'),

    # Liste de tous les cas
    path('cas/', views.liste_cas, name='liste_cas'),

    # Détail d'un cas & Affiche imprimable
    path('cas/<int:pk>/', views.detail_cas, name='detail_cas'),
    path('cas/<int:pk>/affiche/', views.affiche_cas, name='affiche_cas'),

    # Signaler une disparition
    path('signaler/', views.signaler, name='signaler'),

    # Marquer comme retrouvée (admin)
    path('cas/<int:pk>/retrouve/', views.marquer_retrouve, name='marquer_retrouve'),
    path('cas/<int:pk>/valider/', views.valider_cas, name='valider_cas'),
    path('cas/<int:pk>/rejeter/', views.rejeter_cas, name='rejeter_cas'),

    # Carte interactive
    path('carte/', views.carte_disparitions, name='carte'),
]