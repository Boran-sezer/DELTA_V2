# Créer les icônes PWA pour DELTA

## Option 1: Utiliser un générateur en ligne (RECOMMANDÉ)

1. Va sur https://www.pwabuilder.com/imageGenerator
2. Upload une image de DELTA (logo, screenshot, etc.)
3. Télécharge le pack d'icônes
4. Place `icon-192.png` et `icon-512.png` dans `delta_v2/public/`

## Option 2: Créer manuellement

Utilise n'importe quel outil de design (Photoshop, GIMP, Canva, etc.):

1. Crée une image carrée 512x512px
2. Design simple: fond bleu (#3b82f6) avec "DELTA" en blanc
3. Exporte en PNG
4. Redimensionne à 192x192px pour la petite icône
5. Place les fichiers dans `delta_v2/public/`:
   - `icon-192.png` (192x192px)
   - `icon-512.png` (512x512px)

## Option 3: Utiliser un placeholder temporaire

Pour tester rapidement, tu peux utiliser une icône générique:

```bash
# Télécharger des placeholders
curl -o public/icon-192.png https://via.placeholder.com/192/3b82f6/ffffff?text=DELTA
curl -o public/icon-512.png https://via.placeholder.com/512/3b82f6/ffffff?text=DELTA
```

Tu pourras les remplacer plus tard par de vraies icônes!
