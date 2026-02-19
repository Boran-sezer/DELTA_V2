"""
Script pour télécharger les fichiers du modèle Kokoro
"""
import urllib.request
import os

print("Téléchargement des fichiers Kokoro...")

# URLs des fichiers
model_url = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v0_19.onnx"
voices_url = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"

# Télécharger le modèle
print("Téléchargement du modèle kokoro-v0_19.onnx...")
urllib.request.urlretrieve(model_url, "kokoro-v0_19.onnx")
print("✓ Modèle téléchargé")

# Télécharger les voix
print("Téléchargement des voix voices-v1.0.bin...")
urllib.request.urlretrieve(voices_url, "voices_v0_19.bin")
print("✓ Voix téléchargées")

print("\nTous les fichiers sont téléchargés!")
