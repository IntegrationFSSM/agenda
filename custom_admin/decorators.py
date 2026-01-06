from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    """Décorateur pour vérifier si l'utilisateur est administrateur"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.is_admin():
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Accès refusé. Vous devez être administrateur.")
            return redirect('calendar')
    return wrapper


def reservation_permission_required(view_func):
    """Décorateur pour vérifier la permission de créer des réservations"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.has_reservation_permission():
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Vous n'avez pas la permission de créer des réservations.")
            return redirect('calendar')
    return wrapper


def superuser_required(view_func):
    """Décorateur pour vérifier si l'utilisateur est superuser"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Accès refusé. Seuls les super-administrateurs peuvent accéder à cette page.")
            return redirect('calendar')
    return wrapper
