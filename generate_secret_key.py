#!/usr/bin/env python
"""
Script pour générer une clé secrète Django aléatoire et sécurisée
Utilisation: python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("\n" + "="*60)
    print("🔑 NOUVELLE CLÉ SECRÈTE DJANGO GÉNÉRÉE")
    print("="*60)
    print(f"\nSECRET_KEY={secret_key}")
    print("\n" + "="*60)
    print("📋 Copiez cette ligne dans votre fichier .env")
    print("="*60 + "\n")
