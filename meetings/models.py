from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class Participant(models.Model):
    """Modèle pour les participants aux réunions"""
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    organisation = models.CharField(max_length=200, blank=True, verbose_name="Organisation")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Meeting(models.Model):
    """Modèle pour les réunions"""
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(verbose_name="Date de fin")
    lieu = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    
    participants = models.ManyToManyField(
        Participant,
        related_name='reunions',
        verbose_name="Participants",
        blank=True
    )
    
    createur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reunions_creees',
        verbose_name="Créateur"
    )
    
    couleur = models.CharField(
        max_length=7,
        default='#1e40af',
        verbose_name="Couleur",
        help_text="Couleur d'affichage dans le calendrier (format hex)"
    )
    
    notification_envoyee = models.BooleanField(
        default=False,
        verbose_name="Notification envoyée"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Réunion"
        verbose_name_plural = "Réunions"
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"{self.titre} - {self.date_debut.strftime('%d/%m/%Y %H:%M')}"
    
    def envoyer_notifications(self):
        """Envoie les notifications par email aux participants"""
        if not self.participants.exists():
            return
        
        # Préparer le contexte pour le template email
        context = {
            'meeting': self,
            'participants': self.participants.all(),
        }
        
        # Générer le contenu HTML et texte
        html_message = render_to_string('emails/meeting_notification.html', context)
        plain_message = strip_tags(html_message)
        
        # Liste des emails des participants
        recipient_list = list(self.participants.values_list('email', flat=True))
        
        try:
            # Envoyer l'email
            send_mail(
                subject=f"[CIM Agenda] Nouvelle réunion: {self.titre}",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            
            # Marquer comme envoyée
            self.notification_envoyee = True
            self.save(update_fields=['notification_envoyee'])
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi des notifications: {e}")
            return False
    
    def get_participants_emails(self):
        """Retourne la liste des emails des participants"""
        return ", ".join(self.participants.values_list('email', flat=True))
