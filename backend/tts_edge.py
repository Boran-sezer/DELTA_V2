"""
Module TTS Edge pour DELTA
Utilise Microsoft Edge TTS pour une synthèse vocale de qualité
"""

import edge_tts
import asyncio
import threading
import queue
import pyaudio
import io
import time

class EdgeTTS:
    def __init__(self):
        """Initialise le moteur TTS Edge"""
        print("[EDGE-TTS] Initialisation du moteur TTS...")
        
        # Voix française masculine (jeune)
        self.voice = "fr-FR-HenriNeural"  # Voix masculine française
        
        # Queue pour gérer les messages à parler
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.stop_flag = False
        
        # Buffer pour accumuler le texte
        self.text_buffer = []
        self.last_text_time = time.time()
        self.buffer_timeout = 0.5  # Attendre 0.5s avant de parler
        
        # PyAudio pour la lecture
        self.pya = pyaudio.PyAudio()
        
        # Démarrer le thread de parole
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
        print(f"[EDGE-TTS] Moteur TTS initialisé avec voix: {self.voice}")
    
    def _speech_worker(self):
        """Worker thread qui gère la queue de parole"""
        # Créer un event loop pour ce thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while not self.stop_flag:
            try:
                # Vérifier si on doit parler le buffer
                if self.text_buffer and (time.time() - self.last_text_time) > self.buffer_timeout:
                    # Parler tout le buffer accumulé
                    full_text = "".join(self.text_buffer)
                    self.text_buffer = []
                    
                    if full_text.strip():
                        self.is_speaking = True
                        print(f"[EDGE-TTS] Parle: {full_text[:50]}...")
                        
                        try:
                            loop.run_until_complete(self._speak_async(full_text))
                        except Exception as e:
                            print(f"[EDGE-TTS] Erreur: {e}")
                        
                        self.is_speaking = False
                
                # Vérifier la queue
                try:
                    text = self.speech_queue.get(timeout=0.1)
                    if text:
                        self.text_buffer.append(text)
                        self.last_text_time = time.time()
                        self.speech_queue.task_done()
                except queue.Empty:
                    pass
                    
            except Exception as e:
                print(f"[EDGE-TTS] Erreur dans speech_worker: {e}")
        
        loop.close()
    
    async def _speak_async(self, text):
        """Génère et joue l'audio de manière asynchrone"""
        try:
            # Créer le communicator
            communicate = edge_tts.Communicate(text, self.voice)
            
            # Buffer pour accumuler l'audio
            audio_buffer = io.BytesIO()
            
            # Générer l'audio
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
            
            # Jouer l'audio
            audio_data = audio_buffer.getvalue()
            if audio_data:
                stream = self.pya.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,  # Edge TTS utilise 24kHz
                    output=True
                )
                stream.write(audio_data)
                stream.stop_stream()
                stream.close()
        except Exception as e:
            print(f"[EDGE-TTS] Erreur _speak_async: {e}")
    
    def speak(self, text):
        """
        Ajoute du texte à la queue de parole
        Non-bloquant - retourne immédiatement
        """
        if text and text.strip():
            self.speech_queue.put(text.strip())
    
    def clear_queue(self):
        """Vide la queue de parole"""
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
                self.speech_queue.task_done()
            except queue.Empty:
                break
        self.text_buffer = []
        print("[EDGE-TTS] Queue vidée")
    
    def stop(self):
        """Arrête le moteur TTS"""
        self.stop_flag = True
        self.clear_queue()
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)
        self.pya.terminate()
        print("[EDGE-TTS] Moteur TTS arrêté")
    
    def is_busy(self):
        """Retourne True si le TTS est en train de parler"""
        return self.is_speaking or not self.speech_queue.empty() or len(self.text_buffer) > 0


# Instance globale
_edge_tts_instance = None

def get_edge_tts():
    """Retourne l'instance TTS globale (singleton)"""
    global _edge_tts_instance
    if _edge_tts_instance is None:
        _edge_tts_instance = EdgeTTS()
    return _edge_tts_instance
