import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

async def test_cad():
    api_key = os.getenv("GEMINI_API_KEY_1")
    client = genai.Client(http_options={"api_version": "v1beta"}, api_key=api_key)
    model = "gemini-2.0-flash-exp"
    
    prompt = """Génère UNIQUEMENT du code Python exécutable avec build123d pour créer: un cube de 10mm

RÉPONDS AVEC DU CODE SEULEMENT - AUCUN TEXTE AVANT OU APRÈS.

Utilise les formes de base: Box(), Cylinder(), Sphere(), Cone()
Dimensions en millimètres.
Structure:
```python
from build123d import *
with BuildPart() as p:
    [ta forme ici]
result_part = p.part
export_stl(result_part, 'output.stl')
```"""
    
    print("[TEST] Envoi du prompt à Gemini...")
    print(f"[TEST] Modèle: {model}")
    print(f"[TEST] Prompt: {prompt[:100]}...")
    
    raw_content = ""
    stream = await client.aio.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7
        )
    )
    
    async for chunk in stream:
        if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
            for part in chunk.candidates[0].content.parts:
                if part.text:
                    raw_content += part.text
    
    print("\n[TEST] Réponse de Gemini:")
    print("="*80)
    print(raw_content)
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_cad())
