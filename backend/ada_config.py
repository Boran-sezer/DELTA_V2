"""
Configuration pour DELTA
"""

# Mode Audio - Streaming Gemini natif
AUDIO_MODE = "streaming"

# Modèle audio natif
MODEL = "models/gemini-2.5-flash-native-audio-preview-12-2025"

# Audio Settings - Configuration optimisée pour éviter l'effet tunnel
FORMAT_AUDIO = 16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 2048  # Augmenté pour réduire les coupures (était 1024)

# Video Settings
DEFAULT_VIDEO_MODE = "none"

print(f"[CONFIG] Mode: Streaming Gemini Natif")
print(f"[CONFIG] Modèle: {MODEL}")
print(f"[CONFIG] Chunk Size: {CHUNK_SIZE} (optimisé pour audio fluide)")
