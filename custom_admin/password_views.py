from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def change_password_first_login(request):
    """Vue pour changer le mot de passe à la première connexion"""
    
    # Vérifier si l'utilisateur doit vraiment changer son mot de passe
    if not hasattr(request.user, 'profile') or not request.user.profile.must_change_password:
        return redirect('calendar')
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour ne pas déconnecter l'utilisateur
            
            # Marquer que le mot de passe a été changé
            request.user.profile.must_change_password = False
            request.user.profile.save()
            
            messages.success(request, 'Votre mot de passe a été changé avec succès!')
            
            # Rediriger selon le rôle
            if request.user.profile.is_admin():
                return redirect('custom_admin:dashboard')
            else:
                return redirect('calendar')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'auth/change_password_first_login.html', {
        'form': form
    })
