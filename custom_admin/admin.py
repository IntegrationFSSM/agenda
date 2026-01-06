from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Interface d'administration pour les profils utilisateurs"""
    list_display = ['user', 'role', 'can_make_reservation', 'phone', 'created_at']
    list_filter = ['role', 'can_make_reservation', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations', {
            'fields': ('phone',)
        }),
        ('Rôle et Permissions', {
            'fields': ('role', 'can_make_reservation', 'must_change_password')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
