from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from disparitions.models import PersonneDisparue
from .models import Temoignage
from .forms import TemoignageForm

def soumettre(request, personne_id):
    personne = get_object_or_404(PersonneDisparue, pk=personne_id)

    if request.method == 'POST':
        form = TemoignageForm(request.POST)
        if form.is_valid():
            temoignage = form.save(commit=False)
            temoignage.personne = personne
            temoignage.save()
            messages.success(
                request,
                'Merci pour votre témoignage ! '
                'Il sera examiné avant publication.'
            )
            return redirect('detail_cas', pk=personne_id)
    else:
        form = TemoignageForm()

    return render(request, 'temoignages/soumettre.html', {
        'form': form,
        'personne': personne
    })