# ☁️ DELTA Cloud - Guide Complet

## 🎯 Objectif

Héberger DELTA gratuitement sur Fly.io et y accéder depuis ton téléphone comme une vraie app.

## ✅ Ce qui a été préparé

### Fichiers de configuration
- ✅ `Dockerfile` - Containerisation de l'app
- ✅ `fly.toml` - Configuration Fly.io
- ✅ `.dockerignore` - Optimisation du build
- ✅ `manifest.json` - Configuration PWA
- ✅ `sw.js` - Service Worker pour mode offline
- ✅ `index.html` - Meta tags mobile + PWA

### Adaptations
- ✅ Serveur adapté pour cloud (port dynamique, host 0.0.0.0)
- ✅ CSS responsive pour mobile
- ✅ PWA installable sur téléphone
- ✅ Interface touch-friendly

### Scripts et guides
- ✅ `QUICKSTART_CLOUD.md` - Démarrage en 5 minutes
- ✅ `DEPLOY_FLYIO.md` - Guide complet
- ✅ `deploy.ps1` - Script de déploiement automatique
- ✅ `CREATE_ICONS.md` - Guide pour créer les icônes

## 🚀 Démarrage Rapide

### 1. Installer Fly CLI

```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### 2. Se connecter

```bash
fly auth signup  # Ou fly auth login si tu as déjà un compte
```

### 3. Créer les icônes (optionnel pour test)

```bash
# Placeholders temporaires
curl -o public/icon-192.png https://via.placeholder.com/192/3b82f6/ffffff?text=DELTA
curl -o public/icon-512.png https://via.placeholder.com/512/3b82f6/ffffff?text=DELTA
```

### 4. Déployer avec le script automatique

```powershell
.\deploy.ps1
```

Ou manuellement:

```bash
cd delta_v2
fly launch --no-deploy
fly secrets set GEMINI_API_KEY_1="ta_clé"
fly secrets set GEMINI_API_KEY_2="ta_clé_2"
fly deploy
```

### 5. Accéder depuis ton téléphone

1. Obtiens ton URL: `fly status`
2. Ouvre l'URL sur ton téléphone
3. **Android**: Menu → "Ajouter à l'écran d'accueil"
4. **iOS**: Partager → "Sur l'écran d'accueil"

## 📱 Fonctionnalités Mobile

### PWA (Progressive Web App)
- ✅ Installable comme une vraie app
- ✅ Icône sur l'écran d'accueil
- ✅ Plein écran (pas de barre d'adresse)
- ✅ Fonctionne offline (cache basique)

### Interface Responsive
- ✅ Boutons adaptés au touch (44px minimum)
- ✅ Layout adaptatif mobile/desktop
- ✅ Zoom désactivé pour UX native
- ✅ Safe areas iOS respectées

## 💰 Plan Gratuit Fly.io

### Inclus à vie (sans carte bancaire)
- ✅ 3 VMs partagées (256MB RAM)
- ✅ 3GB stockage persistant
- ✅ 160GB bande passante/mois
- ✅ Pas de mise en veille
- ✅ SSL/HTTPS automatique
- ✅ Déploiements illimités

### Limites
- ⚠️ 256MB RAM par VM (suffisant pour DELTA)
- ⚠️ CPU partagé (pas de problème pour usage personnel)
- ⚠️ Pas de GPU (génération CAD côté serveur)

## 🔧 Commandes Utiles

```bash
# Déployer
fly deploy

# Voir les logs
fly logs

# Ouvrir dans le navigateur
fly open

# Voir le statut
fly status

# Lister les secrets
fly secrets list

# Ajouter un secret
fly secrets set KEY="value"

# Redémarrer
fly apps restart

# Arrêter (économiser ressources)
fly scale count 0

# Redémarrer
fly scale count 1
```

## 🐛 Dépannage

### Build échoue
```bash
fly logs
fly deploy --no-cache
```

### App ne démarre pas
```bash
fly logs
fly secrets list  # Vérifier que les clés sont là
```

### Mémoire insuffisante
```bash
fly scale memory 256
```

### Connexion WebSocket échoue
- Vérifie que le CORS est bien configuré
- Vérifie les logs: `fly logs`

## 📊 Monitoring

```bash
# Voir les métriques
fly dashboard

# Logs en temps réel
fly logs -f

# Statut détaillé
fly status --all
```

## 🔄 Mise à jour

Après avoir modifié le code:

```bash
git add .
git commit -m "Update"
fly deploy
```

Ou simplement:

```powershell
.\deploy.ps1
```

## 🎨 Personnalisation

### Changer le nom de l'app
Édite `fly.toml`:
```toml
app = "mon-delta-perso"
```

### Changer la région
```bash
fly regions set cdg  # Paris
fly regions set ams  # Amsterdam
fly regions set lhr  # Londres
```

### Augmenter les ressources (toujours gratuit)
```bash
fly scale memory 256  # Max gratuit
fly scale count 1     # Nombre de VMs
```

## 📱 Tester sur Mobile

### Avant déploiement (local)
1. Trouve ton IP local: `ipconfig`
2. Change `host` dans `server.py` vers ton IP
3. Accède depuis ton téléphone: `http://ton_ip:8000`

### Après déploiement
1. URL publique: `https://ton-app.fly.dev`
2. Accessible depuis n'importe où!

## 🎉 Résultat Final

- ✅ DELTA accessible 24/7 depuis n'importe où
- ✅ Interface adaptée mobile
- ✅ Installable comme app native
- ✅ 100% gratuit à vie
- ✅ Pas de mise en veille
- ✅ SSL/HTTPS automatique
- ✅ Déploiement en 5 minutes

---

**Besoin d'aide?**
- Guide rapide: `QUICKSTART_CLOUD.md`
- Guide complet: `DEPLOY_FLYIO.md`
- Créer icônes: `CREATE_ICONS.md`
