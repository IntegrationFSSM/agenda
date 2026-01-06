from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from .decorators import admin_required
from .forms import UserCreationFormCustom, UserUpdateForm, UserProfileForm
from .models import UserProfile
from meetings.models import Meeting



@admin_required
def admin_dashboard(request):
    """Tableau de bord administrateur"""
    
    # Statistiques
    total_users = User.objects.count()
    total_meetings = Meeting.objects.count()
    users_with_reservation = UserProfile.objects.filter(can_make_reservation=True).count()
    
    # Réunions récentes
    recent_meetings = Meeting.objects.all()[:5]
    
    # Utilisateurs récents
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_meetings': total_meetings,
        'users_with_reservation': users_with_reservation,
        'recent_meetings': recent_meetings,
        'recent_users': recent_users,
    }
    
    return render(request, 'custom_admin/dashboard.html', context)


@admin_required
def admin_users_list(request):
    """Liste des utilisateurs avec filtres"""
    
    users = User.objects.select_related('profile').all()
    
    # Filtres
    search = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    permission_filter = request.GET.get('permission', '')
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    if role_filter:
        users = users.filter(profile__role=role_filter)
    
    if permission_filter == 'yes':
        users = users.filter(profile__can_make_reservation=True)
    elif permission_filter == 'no':
        users = users.filter(profile__can_make_reservation=False)
    
    context = {
        'users': users,
        'search': search,
        'role_filter': role_filter,
        'permission_filter': permission_filter,
        'role_choices': UserProfile.ROLE_CHOICES,
    }
    
    return render(request, 'custom_admin/users_list.html', context)


@admin_required
def admin_user_create(request):
    """Créer un nouvel utilisateur et envoyer les identifiants par email"""
    
    if request.method == 'POST':
        form = UserCreationFormCustom(request.POST)
        if form.is_valid():
            # Sauvegarder l'utilisateur mais garder le mot de passe en clair pour l'email
            user = form.save()
            password = form.cleaned_data.get('password1')
            email = user.email
            
            # Construire le lien de connexion
            login_url = request.build_absolute_uri('/login/')
            
            # Envoyer l'email
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                
                subject = 'Bienvenue sur Agenda CIM - Vos identifiants'
                
                context = {
                    'user': user,
                    'password': password,
                    'login_url': login_url,
                }
                
                html_message = render_to_string('emails/welcome.html', context)
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"--- EMAIL ENVOYÉ À {email} ---")
                messages.success(request, f'Utilisateur {user.email} créé et email envoyé avec succès!')
            except Exception as e:
                import traceback
                print(f"!!! ERREUR ENVOI EMAIL !!!")
                traceback.print_exc()
                messages.warning(request, f'Utilisateur créé mais erreur lors de l\'envoi de l\'email: {str(e)}')
            
            return redirect('custom_admin:users_list')
    else:
        form = UserCreationFormCustom()
    
    return render(request, 'custom_admin/user_form.html', {
        'form': form,
        'title': 'Créer un utilisateur',
        'action': 'create'
    })


@admin_required
def admin_user_update(request, user_id):
    """Modifier un utilisateur"""
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Utilisateur {user.email} modifié avec succès!')
            return redirect('custom_admin:users_list')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)
    
    return render(request, 'custom_admin/user_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': user,
        'title': f'Modifier {user.username}',
        'action': 'update'
    })


@admin_required
def admin_user_delete(request, user_id):
    """Supprimer un utilisateur"""
    
    user = get_object_or_404(User, pk=user_id)
    
    # Empêcher la suppression de son propre compte
    if user == request.user:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte!')
        return redirect('custom_admin:users_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Utilisateur {username} supprimé avec succès!')
        return redirect('custom_admin:users_list')
    
    return render(request, 'custom_admin/user_confirm_delete.html', {
        'user_obj': user
    })


@admin_required
def admin_meetings_manage(request):
    """Gestion des réunions"""
    
    meetings = Meeting.objects.all().order_by('-date_debut')
    
    # Filtres
    search = request.GET.get('search', '')
    if search:
        meetings = meetings.filter(
            Q(titre__icontains=search) |
            Q(description__icontains=search) |
            Q(lieu__icontains=search)
        )
    
    context = {
        'meetings': meetings,
        'search': search,
    }
    
    return render(request, 'custom_admin/meetings_manage.html', context)


@admin_required
def admin_participants_manage(request):
    """Gestion des utilisateurs (anciennement participants)"""
    
    # Rediriger vers la gestion des utilisateurs car Participant n'existe plus
    return redirect('custom_admin:users_list')
