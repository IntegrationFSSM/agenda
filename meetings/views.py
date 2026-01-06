from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from .models import Meeting
from .forms import MeetingForm
from custom_admin.decorators import reservation_permission_required
import json


@login_required
def calendar_view(request):
    """Vue principale du calendrier"""
    meetings = Meeting.objects.all()
    users = User.objects.filter(is_active=True)  # Tous les utilisateurs actifs
    
    # Vérifier si l'utilisateur a la permission de créer des réservations
    can_create = False
    if hasattr(request.user, 'profile'):
        can_create = request.user.profile.has_reservation_permission()
    
    return render(request, 'meetings/calendar.html', {
        'meetings': meetings,
        'users': users,
        'can_create_reservation': can_create,
    })


@login_required
def meeting_list_json(request):
    """API JSON pour FullCalendar - Retourne les réunions au format JSON"""
    meetings = Meeting.objects.all()
    events = []
    
    for meeting in meetings:
        # Les participants sont maintenant des utilisateurs
        participant_names = [f"{p.get_full_name() or p.email}" for p in meeting.participants.all()]
        
        events.append({
            'id': meeting.id,
            'title': meeting.titre,
            'start': meeting.date_debut.isoformat(),
            'end': meeting.date_fin.isoformat(),
            'backgroundColor': meeting.couleur,
            'borderColor': meeting.couleur,
            'description': meeting.description,
            'location': meeting.lieu,
            'participants': participant_names,
        })
    
    return JsonResponse(events, safe=False)


@login_required
def meeting_detail(request, pk):
    """Affiche les détails d'une réunion"""
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meetings/meeting_detail.html', {
        'meeting': meeting
    })


@login_required
@reservation_permission_required
def meeting_create(request):
    """Créer une nouvelle réunion"""
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.createur = request.user
            meeting.save()
            form.save_m2m()  # Sauvegarder les relations ManyToMany (participants)
            
            # Envoyer les notifications
            if meeting.participants.exists():
                meeting.envoyer_notifications()
            
            messages.success(request, 'Réunion créée avec succès!')
            return redirect('calendar')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = MeetingForm()
    
    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'title': 'Créer une réunion'
    })


@login_required
@reservation_permission_required
def meeting_update(request, pk):
    """Modifier une réunion existante"""
    meeting = get_object_or_404(Meeting, pk=pk)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            
            # Envoyer les notifications si nécessaire
            if not meeting.notification_envoyee and meeting.participants.exists():
                meeting.envoyer_notifications()
            
            messages.success(request, 'Réunion modifiée avec succès!')
            return redirect('calendar')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = MeetingForm(instance=meeting)
    
    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'meeting': meeting,
        'title': 'Modifier la réunion'
    })


@login_required
@reservation_permission_required
@require_http_methods(["DELETE", "POST"])
def meeting_delete(request, pk):
    """Supprimer une réunion"""
    meeting = get_object_or_404(Meeting, pk=pk)
    meeting_title = meeting.titre
    
    # Envoyer les notifications d'annulation avant de supprimer
    try:
        if meeting.participants.exists():
            meeting.envoyer_annulation()
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'annulation : {e}")
        
    meeting.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f'Réunion "{meeting_title}" supprimée avec succès'})
    
    messages.success(request, 'Réunion supprimée avec succès!')
    return redirect('calendar')
