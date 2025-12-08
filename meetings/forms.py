from django import forms
from django.forms import DateTimeInput
from .models import Meeting, Participant


class MeetingForm(forms.ModelForm):
    """Formulaire pour créer/modifier une réunion"""
    
    class Meta:
        model = Meeting
        fields = ['titre', 'description', 'date_debut', 'date_fin', 'lieu', 'participants', 'couleur']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la réunion'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description de la réunion'
            }),
            'date_debut': DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'date_fin': DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'lieu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lieu de la réunion'
            }),
            'participants': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'couleur': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
        }
        labels = {
            'titre': 'Titre',
            'description': 'Description',
            'date_debut': 'Date et heure de début',
            'date_fin': 'Date et heure de fin',
            'lieu': 'Lieu',
            'participants': 'Participants',
            'couleur': 'Couleur dans le calendrier',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin:
            if date_fin <= date_debut:
                raise forms.ValidationError(
                    "La date de fin doit être postérieure à la date de début."
                )
        
        return cleaned_data


class ParticipantForm(forms.ModelForm):
    """Formulaire pour ajouter un participant"""
    
    class Meta:
        model = Participant
        fields = ['prenom', 'nom', 'email', 'telephone', 'organisation']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+33 6 12 34 56 78'
            }),
            'organisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organisation'
            }),
        }
        labels = {
            'prenom': 'Prénom',
            'nom': 'Nom',
            'email': 'Email',
            'telephone': 'Téléphone',
            'organisation': 'Organisation',
        }
