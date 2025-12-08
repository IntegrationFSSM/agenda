from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from .models import Meeting, Participant
from .forms import MeetingForm, ParticipantForm
import json


def calendar_view(request):
    """Vue principale du calendrier"""
    meetings = Meeting.objects.all()
    participants = Participant.objects.all()
    return render(request, 'meetings/calendar.html', {
        'meetings': meetings,
        'participants': participants,
    })


def meeting_list_json(request):
    """API JSON pour FullCalendar - Retourne les réunions au format JSON"""
    meetings = Meeting.objects.all()
    events = []
    
    for meeting in meetings:
        events.append({
            'id': meeting.id,
            'title': meeting.titre,
            'start': meeting.date_debut.isoformat(),
            'end': meeting.date_fin.isoformat(),
            'backgroundColor': meeting.couleur,
            'borderColor': meeting.couleur,
            'description': meeting.description,
            'location': meeting.lieu,
            'participants': [p.nom_complet for p in meeting.participants.all()],
        })
    
    return JsonResponse(events, safe=False)


def meeting_detail(request, pk):
    """Affiche les détails d'une réunion"""
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meetings/meeting_detail.html', {
        'meeting': meeting,
    })


def meeting_create(request):
    """Créer une nouvelle réunion"""
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            if request.user.is_authenticated:
                meeting.createur = request.user
            meeting.save()
            form.save_m2m()  # Sauvegarder les relations ManyToMany
            
            # Envoyer les notifications
            if meeting.participants.exists():
                meeting.envoyer_notifications()
                messages.success(request, 'Réunion créée et notifications envoyées avec succès!')
            else:
                messages.success(request, 'Réunion créée avec succès!')
            
            return redirect('calendar')
        else:
            messages.error(request, 'Erreur lors de la création de la réunion.')
    else:
        form = MeetingForm()
    
    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'title': 'Nouvelle réunion'
    })


def meeting_update(request, pk):
    """Modifier une réunion existante"""
    meeting = get_object_or_404(Meeting, pk=pk)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            
            # Envoyer les notifications si modifications
            if meeting.participants.exists():
                meeting.notification_envoyee = False
                meeting.save()
                meeting.envoyer_notifications()
                messages.success(request, 'Réunion mise à jour et notifications envoyées!')
            else:
                messages.success(request, 'Réunion mise à jour avec succès!')
            
            return redirect('calendar')
        else:
            messages.error(request, 'Erreur lors de la mise à jour.')
    else:
        form = MeetingForm(instance=meeting)
    
    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'meeting': meeting,
        'title': 'Modifier la réunion'
    })


@require_http_methods(["DELETE", "POST"])
def meeting_delete(request, pk):
    """Supprimer une réunion"""
    meeting = get_object_or_404(Meeting, pk=pk)
    meeting.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    messages.success(request, 'Réunion supprimée avec succès!')
    return redirect('calendar')


def participant_list(request):
    """Liste des participants"""
    participants = Participant.objects.all()
    return render(request, 'meetings/participant_list.html', {
        'participants': participants,
    })


def participant_create(request):
    """Créer un nouveau participant"""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant ajouté avec succès!')
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    
    return render(request, 'meetings/participant_form.html', {
        'form': form,
        'title': 'Nouveau participant'
    })


def participant_update(request, pk):
    """Modifier un participant"""
    participant = get_object_or_404(Participant, pk=pk)
    
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant mis à jour avec succès!')
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    
    return render(request, 'meetings/participant_form.html', {
        'form': form,
        'participant': participant,
        'title': 'Modifier le participant'
    })


@require_http_methods(["DELETE", "POST"])
def participant_delete(request, pk):
    """Supprimer un participant"""
    participant = get_object_or_404(Participant, pk=pk)
    participant.delete()
    messages.success(request, 'Participant supprimé avec succès!')
    return redirect('participant_list')
