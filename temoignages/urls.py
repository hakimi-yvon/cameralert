from django.urls import path
from . import views

urlpatterns = [
    path('soumettre/<int:personne_id>/', views.soumettre, name='soumettre_temoignage'),
    path('<int:pk>/valider/', views.valider_temoignage, name='valider_temoignage'),
    path('<int:pk>/supprimer/', views.supprimer_temoignage, name='supprimer_temoignage'),
]