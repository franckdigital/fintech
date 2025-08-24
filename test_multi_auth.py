#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour l'authentification multi-champs (email/téléphone)
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_login(username, password, description):
    """Test de connexion avec username et password"""
    url = f"{BASE_URL}/api/auth/login/"
    data = {
        "email": username,  # Le champ s'appelle "email" mais accepte email ou téléphone
        "password": password
    }
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"\n=== Test: {description} ===")
        print(f"Username: {username}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Connexion réussie!")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            try:
                result = response.json()
                print(f"[ERREUR] Connexion échouée")
                print(f"Response: {json.dumps(result, indent=2)}")
            except:
                print(f"[ERREUR] Réponse non-JSON: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"[ERREUR] Erreur de connexion - Serveur non disponible")
        return False
    except Exception as e:
        print(f"[ERREUR] Erreur: {str(e)}")
        return False

def main():
    print("Test d'authentification multi-champs XAMILA")
    print("=" * 50)
    
    # Test 1: Connexion par email
    test_login("test@xamila.com", "test123", "Connexion par email")
    
    # Test 2: Connexion par téléphone (format normalisé)
    test_login("+33123456789", "test123", "Connexion par téléphone (+33)")
    
    # Test 2b: Connexion par téléphone (format français)
    test_login("0123456789", "test123", "Connexion par téléphone (0123)")
    
    # Test 2c: Connexion par téléphone (format international sans +)
    test_login("33123456789", "test123", "Connexion par téléphone (33 sans +)")
    
    # Test 3: Mauvais mot de passe
    test_login("test@xamila.com", "wrongpassword", "Mauvais mot de passe")
    
    # Test 4: Utilisateur inexistant
    test_login("inexistant@xamila.com", "test123", "Utilisateur inexistant")
    
    print("\n" + "=" * 50)
    print("Tests terminés!")

if __name__ == "__main__":
    main()
