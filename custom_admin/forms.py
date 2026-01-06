from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserCreationFormCustom(UserCreationForm):
    """Formulaire de création d'utilisateur avec profil - Email comme nom d'utilisateur"""
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (sera utilisé comme identifiant)'})
    )
    
    # Champs du profil
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone (optionnel)'})
    )
    
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    can_make_reservation = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Retirer le champ username du formulaire
        if 'username' in self.fields:
            del self.fields['username']
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
        
        # Désactiver les validateurs de mot de passe pour l'admin
        # L'utilisateur devra changer son mot de passe à la première connexion avec des contraintes strictes
        self.fields['password1'].help_text = "L'utilisateur devra changer ce mot de passe à la première connexion."
        self.fields['password2'].help_text = None
    
    def clean_email(self):
        """Vérifier que l'email est unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
        return email
    
    def _post_clean(self):
        """Override pour désactiver la validation de mot de passe pour l'admin"""
        # Ne pas appeler super()._post_clean() pour éviter la validation du mot de passe
        # L'utilisateur devra changer son mot de passe à la première connexion
        pass
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)  # Bypass UserCreationForm validation
        email = self.cleaned_data['email']
        
        # Utiliser l'email comme username
        user.username = email
        user.email = email
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            # Mettre à jour le profil
            profile = user.profile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.role = self.cleaned_data.get('role', 'USER')
            profile.can_make_reservation = self.cleaned_data.get('can_make_reservation', False)
            profile.save()
        
        return user


class UserUpdateForm(forms.ModelForm):
    """Formulaire de modification d'utilisateur - Email comme identifiant"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_email(self):
        """Vérifier que l'email est unique (sauf pour l'utilisateur actuel)"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Synchroniser username avec email
        user.username = user.email
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Formulaire de modification du profil utilisateur - Sans organisation"""
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'role', 'can_make_reservation']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'can_make_reservation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
