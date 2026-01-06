from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Profil utilisateur étendu avec permissions et rôles"""
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('USER', 'Utilisateur'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Utilisateur"
    )
    
    # Informations supplémentaires
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    
    # Rôle et permissions
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='USER',
        verbose_name="Rôle"
    )
    
    can_make_reservation = models.BooleanField(
        default=False,
        verbose_name="Peut créer des réservations"
    )
    
    must_change_password = models.BooleanField(
        default=True,
        verbose_name="Doit changer le mot de passe",
        help_text="L'utilisateur doit changer son mot de passe à la première connexion"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Profil Utilisateur"
        verbose_name_plural = "Profils Utilisateurs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    def is_admin(self):
        """Vérifie si l'utilisateur est administrateur"""
        return self.role == 'ADMIN' or self.user.is_superuser
    
    def has_reservation_permission(self):
        """Vérifie si l'utilisateur peut créer des réservations"""
        return self.can_make_reservation or self.is_admin()
    
    @property
    def full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil lors de la création d'un utilisateur"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil lors de la sauvegarde de l'utilisateur"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
