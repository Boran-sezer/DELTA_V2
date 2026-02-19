# 🚀 Démarrage Rapide - DELTA Cloud

## En 5 minutes, ton DELTA sera accessible depuis ton téléphone!

### Étape 1: Installer Fly CLI (2 min)

**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

Redémarre ton terminal après installation.

### Étape 2: Créer un compte Fly.io (1 min)

```bash
fly auth signup
```

Ou va sur https://fly.io/app/sign-up

✅ **Gratuit à vie, pas de carte bancaire nécessaire!**

### Étape 3: Se connecter (30 sec)

```bash
fly auth login
```

### Étape 4: Déployer DELTA (2 min)

```bash
cd delta_v2

# Lancer l'app (première fois)
fly launch --no-deploy

# Configurer tes clés Gemini
fly secrets set GEMINI_API_KEY_1="ta_clé_gemini_1"
fly secrets set GEMINI_API_KEY_2="ta_clé_gemini_2"

# Déployer!
fly deploy
```

### Étape 5: Accéder depuis ton téléphone! (30 sec)

```bash
# Obtenir ton URL
fly status
```

Ton URL: `https://ton-app.fly.dev`

**Sur ton téléphone:**
1. Ouvre l'URL dans Chrome/Safari
2. Menu → "Ajouter à l'écran d'accueil"
3. 🎉 DELTA est maintenant une app sur ton téléphone!

---

## ✅ C'est tout!

- ✅ Accessible 24/7 depuis n'importe où
- ✅ Interface adaptée mobile
- ✅ Installable comme une vraie app
- ✅ 100% gratuit à vie
- ✅ Pas de mise en veille

## Commandes utiles

```bash
# Voir les logs
fly logs

# Ouvrir dans le navigateur
fly open

# Redéployer après modifications
fly deploy
```

## Besoin d'aide?

Consulte `DEPLOY_FLYIO.md` pour le guide complet.
