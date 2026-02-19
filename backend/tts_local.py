"""
Module TTS Local pour DELTA
Utilise pyttsx3 pour une synthèse vocale locale sans coupures
"""

import pyttsx3
import threading
import queue
import time

class LocalTTS:
    def __init__(self):
        """Initialise le moteur TTS local"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 165)  # Vitesse de parole (150-200 normal)
        self.engine.setProperty('volume', 1.0)  # Volume max
        
        # Essayer de trouver une voix française
        voices = self.engine.getProperty('voices')
        french_voice_found = False
        
        for voice in voices:
            # Chercher une voix française
            if 'french' in voice.name.lower() or 'fr' in voice.id.lower() or 'hortense' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                french_voice_found = True
                print(f"[TTS] Voix française trouvée: {voice.name}")
                break
        
        if not french_voice_found:
            print("[TTS] Aucune voix française trouvée, utilisation de la voix par défaut")
            # Utiliser la première voix disponible
            if voices:
                self.engine.setProperty('voice', voices[0].id)
                print(f"[TTS] Voix par défaut: {voices[0].name}")
        
        # Queue pour gérer les messages à parler
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.stop_flag = False
        
        # Démarrer le thread de parole
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
        print("[TTS] Moteur TTS local initialisé")
    
    def _speech_worker(self):
        """Worker thread qui gère la queue de parole"""
        while not self.stop_flag:
            try:
                # Attendre un message (timeout pour vérifier stop_flag)
                text = self.speech_queue.get(timeout=0.5)
                
                if text:
                    self.is_speaking = True
                    print(f"[TTS] Parle: {text[:50]}...")
                    
                    try:
                        self.engine.say(text)
                        self.engine.runAndWait()
                    except Exception as e:
                        print(f"[TTS] Erreur lors de la parole: {e}")
                    
                    self.is_speaking = False
                    self.speech_queue.task_done()
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[TTS] Erreur dans speech_worker: {e}")
    
    def speak(self, text):
        """
        Ajoute du texte à la queue de parole
        Non-bloquant - retourne immédiatement
        """
        if text and text.strip():
            self.speech_queue.put(text.strip())
    
    def speak_now(self, text):
        """
        Parle immédiatement (bloquant)
        Utile pour les messages importants
        """
        if text and text.strip():
            self.is_speaking = True
            print(f"[TTS] Parle immédiatement: {text[:50]}...")
            try:
                self.engine.say(text.strip())
                self.engine.runAndWait()
            except Exception as e:
                print(f"[TTS] Erreur: {e}")
            self.is_speaking = False
    
    def clear_queue(self):
        """Vide la queue de parole"""
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
                self.speech_queue.task_done()
            except queue.Empty:
                break
        print("[TTS] Queue vidée")
    
    def stop(self):
        """Arrête le moteur TTS"""
        self.stop_flag = True
        self.clear_queue()
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)
        print("[TTS] Moteur TTS arrêté")
    
    def is_busy(self):
        """Retourne True si le TTS est en train de parler"""
        return self.is_speaking or not self.speech_queue.empty()


# Instance globale
_tts_instance = None

def get_tts():
    """Retourne l'instance TTS globale (singleton)"""
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = LocalTTS()
    return _tts_instance


if __name__ == "__main__":
    # Test du module
    print("Test du module TTS Local")
    tts = LocalTTS()
    
    tts.speak("Bonjour, je suis DELTA, votre assistant de design.")
    time.sleep(1)
    tts.speak("Je peux maintenant parler sans coupures grâce à la synthèse vocale locale.")
    
    # Attendre que tout soit dit
    while tts.is_busy():
        time.sleep(0.1)
    
    print("Test terminé")
    tts.stop()
