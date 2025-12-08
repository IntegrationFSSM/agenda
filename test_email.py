#!/usr/bin/env python
"""
Script de test pour vérifier la configuration email
Utilisation: python test_email.py
"""

import os
import sys
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenda_cim.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings


def test_email_connection():
    """Teste la connexion et l'envoi d'un email"""
    print("\n" + "="*70)
    print("🧪 TEST DE CONFIGURATION EMAIL")
    print("="*70)
    
    # Vérifier la configuration
    print("\n📋 Configuration actuelle :")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or '(non défini)'}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Vérifier si les credentials sont configurés
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ ERREUR : Email ou mot de passe non configuré dans .env")
        print("\n💡 Ajoutez ces lignes dans votre fichier .env :")
        print("   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
        print("   EMAIL_HOST_USER=votre-email@gmail.com")
        print("   EMAIL_HOST_PASSWORD=votre-mot-de-passe-application")
        print("\nConsultez GUIDE_CONFIGURATION_GMAIL.md pour plus d'infos.")
        return False
    
    # Vérifier le backend
    if 'console' in settings.EMAIL_BACKEND.lower():
        print("\n⚠️  ATTENTION : EMAIL_BACKEND est configuré pour la console")
        print("   Les emails s'afficheront dans le terminal au lieu d'être envoyés.")
        print("\n💡 Pour envoyer de vrais emails, modifiez .env :")
        print("   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
        return False
    
    # Demander l'email de destination
    print("\n" + "="*70)
    email_dest = input("📧 Entrez votre email pour recevoir l'email de test : ").strip()
    
    if not email_dest:
        print("❌ Email non fourni. Test annulé.")
        return False
    
    # Envoyer l'email de test
    print(f"\n📤 Envoi d'un email de test à {email_dest}...")
    
    try:
        send_mail(
            subject='[CIM Agenda] Test de configuration email',
            message='Félicitations ! Votre configuration email fonctionne correctement. '
                   'Vous pouvez maintenant envoyer des notifications de réunion.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_dest],
            fail_silently=False,
        )
        
        print("\n✅ EMAIL ENVOYÉ AVEC SUCCÈS !")
        print(f"   Vérifiez votre boîte de réception : {email_dest}")
        print("   (Vérifiez aussi le dossier spam)")
        print("\n🎉 Configuration email validée !")
        return True
        
    except Exception as e:
        print("\n❌ ERREUR lors de l'envoi de l'email :")
        print(f"   {type(e).__name__}: {str(e)}")
        
        # Diagnostics
        print("\n🔍 Diagnostics :")
        
        if "Authentication" in str(e):
            print("   ❌ Erreur d'authentification Gmail")
            print("   💡 Solutions :")
            print("      1. Vérifiez que la validation en 2 étapes est activée")
            print("      2. Générez un nouveau mot de passe d'application")
            print("      3. Copiez le mot de passe SANS espaces")
            print("      4. Vérifiez EMAIL_HOST_USER et EMAIL_HOST_PASSWORD dans .env")
        
        elif "Connection" in str(e) or "Timeout" in str(e):
            print("   ❌ Problème de connexion")
            print("   💡 Solutions :")
            print("      1. Vérifiez votre connexion Internet")
            print("      2. Vérifiez que le port 587 n'est pas bloqué")
            print("      3. Essayez de désactiver temporairement votre antivirus/pare-feu")
        
        else:
            print("   ℹ️  Consultez GUIDE_CONFIGURATION_GMAIL.md pour plus d'aide")
        
        return False
    
    finally:
        print("\n" + "="*70)


if __name__ == "__main__":
    success = test_email_connection()
    sys.exit(0 if success else 1)
