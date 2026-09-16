from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
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

from django.views.decorators.http import require_POST

@staff_member_required
@require_POST
def valider_temoignage(request, pk):
    temoignage = get_object_or_404(Temoignage, pk=pk)
    temoignage.est_valide = True
    temoignage.save()
    messages.success(request, 'Le témoignage a été validé et publié.')
    return redirect('dashboard')

@staff_member_required
@require_POST
def supprimer_temoignage(request, pk):
    temoignage = get_object_or_404(Temoignage, pk=pk)
    temoignage.delete()
    messages.warning(request, 'Le témoignage a été supprimé.')
    return redirect('dashboard')