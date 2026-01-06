from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    """Vue de connexion - Utilise l'email comme identifiant"""
    if request.user.is_authenticated:
        return redirect('calendar')
    
    if request.method == 'POST':
        email = request.POST.get('username')  # Le champ s'appelle 'username' dans le formulaire mais contient l'email
        password = request.POST.get('password')
        
        # Chercher l'utilisateur par email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = email  # Si pas trouvé, essayer quand même
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Vérifier si l'utilisateur doit changer son mot de passe
            if hasattr(user, 'profile') and user.profile.must_change_password:
                messages.warning(request, 'Vous devez changer votre mot de passe avant de continuer.')
                return redirect('change_password_first_login')
            
            messages.success(request, f'Bienvenue {user.get_full_name() or user.email}!')
            
            # Redirection selon le rôle
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            elif hasattr(user, 'profile') and user.profile.is_admin():
                return redirect('custom_admin:dashboard')
            else:
                return redirect('calendar')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')


@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    return render(request, 'auth/profile.html', {
        'user': request.user,
        'profile': request.user.profile if hasattr(request.user, 'profile') else None
    })
