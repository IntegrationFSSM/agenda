from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    """Modèle pour les réunions - Les participants sont des utilisateurs"""
    
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(verbose_name="Date de fin")
    lieu = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    
    participants = models.ManyToManyField(
        User,
        related_name='reunions',
        verbose_name="Participants",
        blank=True
    )
    
    createur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reunions_creees',
        verbose_name="Créateur"
    )
    
    couleur = models.CharField(
        max_length=7,
        default='#007bff',
        verbose_name="Couleur"
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
        """Envoie un email d'invitation HTML à tous les participants"""
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        
        subject = f"Invitation : {self.titre}"
        
        # Liste des emails des participants
        emails = [p.email for p in self.participants.all() if p.email]
        
        if not emails:
            return
            
        # Contexte pour le template
        context = {
            'meeting': self,
            'login_url': 'http://127.0.0.1:8000/login/', # Idéalement utiliser Site.objects.get_current().domain
        }
        
        try:
            print(f"--- PRÉPARATION EMAIL HTML POUR {len(emails)} PARTICIPANTS ---")
            
            # Générer le contenu HTML et Texte
            html_message = render_to_string('emails/invitation.html', context)
            plain_message = strip_tags(html_message)
            
            # Envoyer à chaque participant pour personnaliser (cher) ou en Bcc (rapide)
            # Ici on envoie en boucle pour personnaliser le nom dans le template si possible
            # Mais le template actuel attend 'user' pour dire 'Bonjour X'.
            # On va donc itérer sur les participants.
            
            for participant in self.participants.all():
                if not participant.email:
                    continue
                    
                context['user'] = participant
                html_content = render_to_string('emails/invitation.html', context)
                text_content = strip_tags(html_content)
                
                send_mail(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [participant.email],
                    html_message=html_content,
                    fail_silently=False,
                )
                
            self.notification_envoyee = True
            self.save()
            print("--- INVITATIONS HTML ENVOYÉES AVEC SUCCÈS ---")
        except Exception as e:
            import traceback
            print("!!! ERREUR ENVOI INVITATION !!!")
            traceback.print_exc()
            pass

    def envoyer_annulation(self):
        """Envoie un email d'annulation avant la suppression"""
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        
        subject = f"ANNULATION : {self.titre}"
        
        # Sauvegarder les infos avant suppression
        context = {
            'meeting_title': self.titre,
            'meeting_date': self.date_debut.strftime('%d/%m/%Y à %H:%M'),
            'meeting_location': self.lieu or 'Non précisé',
            'login_url': 'http://127.0.0.1:8000/login/',
        }
        
        try:
            print(f"--- ENVOI ANNULATION POUR {self.titre} ---")
            for participant in self.participants.all():
                if not participant.email:
                    continue
                    
                context['user'] = participant
                html_content = render_to_string('emails/cancellation.html', context)
                text_content = strip_tags(html_content)
                
                send_mail(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [participant.email],
                    html_message=html_content,
                    fail_silently=False,
                )
            print("--- NOTIFICATIONS ANNULATION ENVOYÉES ---")
        except Exception as e:
            print(f"Erreur envoi annulation: {e}")
            pass
