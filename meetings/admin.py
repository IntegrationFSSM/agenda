from django.contrib import admin
from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Interface d'administration pour les réunions"""
    list_display = ['titre', 'date_debut', 'date_fin', 'lieu', 'createur', 'notification_envoyee']
    search_fields = ['titre', 'description', 'lieu']
    list_filter = ['date_debut', 'notification_envoyee', 'createur']
    filter_horizontal = ['participants']
    ordering = ['-date_debut']
    date_hierarchy = 'date_debut'
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'description', 'couleur')
        }),
        ('Date et lieu', {
            'fields': ('date_debut', 'date_fin', 'lieu')
        }),
        ('Participants', {
            'fields': ('participants',)
        }),
        ('Métadonnées', {
            'fields': ('createur', 'notification_envoyee'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Définit automatiquement le créateur si nouveau"""
        if not obj.pk and not obj.createur:
            obj.createur = request.user
        super().save_model(request, obj, form, change)
