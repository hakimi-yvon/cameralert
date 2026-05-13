from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import InscriptionForm
from django.contrib import messages

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès !')
            return redirect('accueil')
    else:
        form = InscriptionForm()

    return render(request, 'comptes/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accueil')
    else:
        form = AuthenticationForm()

    return render(request, 'comptes/connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('accueil')