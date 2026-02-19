# 🚀 Déploiement DELTA sur Fly.io

## Prérequis

1. **Créer un compte Fly.io** (gratuit à vie):
   - Va sur https://fly.io/app/sign-up
   - Inscris-toi avec ton email
   - Pas besoin de carte bancaire!

2. **Installer Fly CLI**:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Ou avec Chocolatey
   choco install flyctl
   ```

3. **Se connecter**:
   ```bash
   fly auth login
   ```

## Étapes de déploiement

### 1. Préparer les variables d'environnement

Créer un fichier `.env.production` avec tes clés API:

```env
GEMINI_API_KEY_1=ta_clé_gemini_1
GEMINI_API_KEY_2=ta_clé_gemini_2
```

### 2. Créer l'application Fly.io

```bash
cd delta_v2
fly launch --no-deploy
```

Répondre aux questions:
- App name: `delta-assistant` (ou ton choix)
- Region: `cdg` (Paris) ou `ams` (Amsterdam)
- PostgreSQL: **Non**
- Redis: **Non**

### 3. Configurer les secrets (variables d'environnement)

```bash
# Ajouter tes clés Gemini
fly secrets set GEMINI_API_KEY_1="ta_clé_1"
fly secrets set GEMINI_API_KEY_2="ta_clé_2"
```

### 4. Déployer!

```bash
fly deploy
```

Le déploiement prend 5-10 minutes la première fois.

### 5. Obtenir l'URL

```bash
fly status
```

Ton URL sera: `https://delta-assistant.fly.dev` (ou le nom que tu as choisi)

## Accès depuis ton téléphone

### Option 1: Navigateur web
1. Ouvre `https://ton-app.fly.dev` sur ton téléphone
2. L'interface est responsive et adaptée mobile

### Option 2: Installer comme app (PWA)
1. Ouvre l'URL dans Chrome/Safari
2. **Android**: Menu → "Ajouter à l'écran d'accueil"
3. **iOS**: Partager → "Sur l'écran d'accueil"
4. L'app s'ouvre en plein écran comme une vraie app!

## Commandes utiles

```bash
# Voir les logs en temps réel
fly logs

# Ouvrir l'app dans le navigateur
fly open

# Voir le statut
fly status

# Redéployer après modifications
fly deploy

# Arrêter l'app (économiser ressources)
fly scale count 0

# Redémarrer l'app
fly scale count 1
```

## Plan gratuit Fly.io

✅ **Inclus gratuitement à vie**:
- 3 VMs partagées (256MB RAM chacune)
- 3GB de stockage persistant
- 160GB de bande passante sortante/mois
- Pas de mise en veille automatique
- SSL/HTTPS automatique

## Problèmes courants

### Build échoue
```bash
# Vérifier les logs
fly logs

# Rebuild complet
fly deploy --no-cache
```

### App ne démarre pas
```bash
# Vérifier les secrets
fly secrets list

# Voir les logs de démarrage
fly logs
```

### Mémoire insuffisante
```bash
# Augmenter la RAM (toujours gratuit jusqu'à 256MB)
fly scale memory 256
```

## Mise à jour de l'app

Après avoir modifié le code:

```bash
git add .
git commit -m "Update"
fly deploy
```

## Supprimer l'app

```bash
fly apps destroy delta-assistant
```

---

## 🎉 C'est tout!

Ton DELTA est maintenant accessible 24/7 depuis n'importe où dans le monde, gratuitement!

URL: `https://ton-app.fly.dev`
