from django.urls import path
from . import views

urlpatterns = [
    path('soumettre/<int:personne_id>/', views.soumettre, name='soumettre_temoignage'),
]