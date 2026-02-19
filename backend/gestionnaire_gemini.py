"""
Gestionnaire Multi-Gemini pour DELTA V2
Rotation automatique entre plusieurs clés API pour quotas illimités
"""

import os
import time
from typing import Optional, List
from google import genai
from google.genai import types

class GestionnaireGemini:
    def __init__(self):
        self.cles_api = self._charger_cles()
        self.index_actuel = 0
        self.derniere_rotation = {}
        self.delai_rotation = 60  # Secondes avant de réessayer une clé
        
        if not self.cles_api:
            raise ValueError("Aucune cle Gemini trouvee dans .env")
        
        print(f"[OK] {len(self.cles_api)} cle(s) Gemini chargee(s)".encode('utf-8', errors='replace').decode('utf-8'))
        self.client = self._creer_client()
    
    def _charger_cles(self) -> List[str]:
        """Charge toutes les clés GEMINI_API_KEY_X depuis .env"""
        cles = []
        i = 1
        while True:
            cle = os.getenv(f"GEMINI_API_KEY_{i}")
            if not cle:
                break
            cles.append(cle)
            i += 1
        return cles
    
    def _creer_client(self):
        """Crée un client Gemini avec la clé actuelle"""
        cle = self.cles_api[self.index_actuel]
        # Utiliser v1beta pour les modèles audio natifs
        return genai.Client(http_options={"api_version": "v1beta"}, api_key=cle)
    
    def rotation_cle(self):
        """Passe à la clé suivante"""
        ancien_index = self.index_actuel
        self.derniere_rotation[ancien_index] = time.time()
        
        # Essayer les clés suivantes
        for _ in range(len(self.cles_api)):
            self.index_actuel = (self.index_actuel + 1) % len(self.cles_api)
            
            # Vérifier si cette clé peut être réutilisée
            derniere_utilisation = self.derniere_rotation.get(self.index_actuel, 0)
            if time.time() - derniere_utilisation > self.delai_rotation:
                print(f"[ROTATION] Vers cle Gemini #{self.index_actuel + 1}")
                self.client = self._creer_client()
                return True
        
        print("[ATTENTION] Toutes les cles sont en cooldown, attente...")
        time.sleep(5)
        return False
    
    def obtenir_client(self):
        """Retourne le client Gemini actuel"""
        return self.client
    
    def executer_avec_retry(self, fonction, *args, **kwargs):
        """Exécute une fonction avec retry automatique sur erreur de quota"""
        tentatives = len(self.cles_api)
        
        for tentative in range(tentatives):
            try:
                return fonction(*args, **kwargs)
            except Exception as e:
                erreur = str(e).lower()
                
                # Erreurs de quota
                if "quota" in erreur or "rate limit" in erreur or "429" in erreur:
                    print(f"[ATTENTION] Quota atteint sur cle #{self.index_actuel + 1}")
                    
                    if tentative < tentatives - 1:
                        self.rotation_cle()
                        continue
                    else:
                        raise Exception("Toutes les cles Gemini ont atteint leur quota")
                else:
                    # Autre erreur, ne pas faire de rotation
                    raise e
        
        raise Exception("Échec après toutes les tentatives")
