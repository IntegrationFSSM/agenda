from django import forms
from django.contrib.auth.models import User
from .models import Meeting


class MeetingForm(forms.ModelForm):
    """Formulaire pour créer/modifier une réunion"""
    
    # Les participants sont maintenant des utilisateurs
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True).order_by('first_name', 'last_name', 'email'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'participants-select'}),
        required=False,
        label="Participants",
        help_text="Recherchez et ajoutez des participants"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser l'affichage des utilisateurs
        self.fields['participants'].label_from_instance = lambda obj: f"{obj.get_full_name()} ({obj.email})" if obj.get_full_name() else obj.email
    
    class Meta:
        model = Meeting
        fields = ['titre', 'description', 'date_debut', 'date_fin', 'lieu', 'participants']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la réunion'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'date_debut': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'date_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de la réunion'}),
        }
        labels = {
            'titre': 'Titre',
            'description': 'Description',
            'date_debut': 'Date de début',
            'date_fin': 'Date de fin',
            'lieu': 'Lieu',
        }
