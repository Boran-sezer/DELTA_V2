"""
Module TTS Kokoro pour DELTA
Utilise Kokoro-82M pour une synthèse vocale de qualité
"""

import kokoro_onnx
import threading
import queue
import io
import pyaudio

class KokoroTTS:
    def __init__(self):
        """Initialise le moteur TTS Kokoro"""
        print("[KOKORO] Initialisation du moteur TTS...")
        
        # Initialiser Kokoro avec voix française masculine
        self.tts = kokoro_onnx.Kokoro("kokoro-v0_19.onnx", "voices_v0_19.bin")
        
        # Configuration audio
        self.sample_rate = 24000  # Kokoro utilise 24kHz
        
        # Queue pour gérer les messages à parler
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.stop_flag = False
        
        # PyAudio pour la lecture
        self.pya = pyaudio.PyAudio()
        
        # Démarrer le thread de parole
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
        print("[KOKORO] Moteur TTS initialisé avec succès")
    
    def _speech_worker(self):
        """Worker thread qui gère la queue de parole"""
        while not self.stop_flag:
            try:
                # Attendre un message (timeout pour vérifier stop_flag)
                text = self.speech_queue.get(timeout=0.5)
                
                if text:
                    self.is_speaking = True
                    print(f"[KOKORO] Parle: {text[:50]}...")
                    
                    try:
                        # Générer l'audio avec Kokoro
                        samples, sample_rate = self.tts.create(text, voice="af_bella", speed=1.0, lang="fr-fr")
                        
                        # Convertir en bytes pour PyAudio
                        audio_data = (samples * 32767).astype('int16').tobytes()
                        
                        # Jouer l'audio
                        stream = self.pya.open(
                            format=pyaudio.paInt16,
                            channels=1,
                            rate=sample_rate,
                            output=True
                        )
                        stream.write(audio_data)
                        stream.stop_stream()
                        stream.close()
                        
                    except Exception as e:
                        print(f"[KOKORO] Erreur lors de la parole: {e}")
                    
                    self.is_speaking = False
                    self.speech_queue.task_done()
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[KOKORO] Erreur dans speech_worker: {e}")
    
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
        print("[KOKORO] Queue vidée")
    
    def stop(self):
        """Arrête le moteur TTS"""
        self.stop_flag = True
        self.clear_queue()
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)
        self.pya.terminate()
        print("[KOKORO] Moteur TTS arrêté")
    
    def is_busy(self):
        """Retourne True si le TTS est en train de parler"""
        return self.is_speaking or not self.speech_queue.empty()


# Instance globale
_kokoro_instance = None

def get_kokoro_tts():
    """Retourne l'instance TTS globale (singleton)"""
    global _kokoro_instance
    if _kokoro_instance is None:
        _kokoro_instance = KokoroTTS()
    return _kokoro_instance
