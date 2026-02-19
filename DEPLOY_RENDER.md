# 🚀 Déployer DELTA sur Render.com (100% Gratuit)

## Pourquoi Render.com?
- ✅ **Vraiment gratuit** (pas de carte bancaire)
- ✅ **Tout dans le navigateur** (pas de commandes)
- ✅ **Très simple** (5 minutes)
- ⚠️ L'app s'endort après 15min d'inactivité (redémarre en 30 secondes)

---

## 📝 Étapes (5 minutes)

### 1. Créer un compte GitHub (si tu n'en as pas)

Va sur https://github.com/signup et crée un compte gratuit.

### 2. Mettre ton code sur GitHub

**Option A: Via GitHub Desktop (plus simple)**
1. Télécharge GitHub Desktop: https://desktop.github.com/
2. Installe et connecte-toi
3. File → Add Local Repository → Choisis le dossier `delta_v2`
4. Clique sur "Publish repository"
5. Décoche "Keep this code private" si tu veux (ou laisse coché)
6. Clique sur "Publish repository"

**Option B: Via ligne de commande**
```bash
cd delta_v2
git init
git add .
git commit -m "Initial commit"
git branch -M main
# Crée un repo sur github.com puis:
git remote add origin https://github.com/TON_USERNAME/delta.git
git push -u origin main
```

### 3. Créer un compte Render.com

1. Va sur https://render.com/
2. Clique sur "Get Started for Free"
3. Connecte-toi avec ton compte GitHub (c'est plus simple)

### 4. Déployer DELTA

1. Sur Render.com, clique sur "New +"
2. Choisis "Web Service"
3. Connecte ton repository GitHub `delta`
4. Render détecte automatiquement le Dockerfile
5. Configure:
   - **Name**: `delta-boran` (ou ce que tu veux)
   - **Region**: Frankfurt (Europe)
   - **Branch**: main
   - **Plan**: Free
6. Clique sur "Advanced"
7. Ajoute les variables d'environnement:
   - `GEMINI_API_KEY_1` = `ta_clé_1`
   - `GEMINI_API_KEY_2` = `ta_clé_2`
8. Clique sur "Create Web Service"

### 5. Attendre le déploiement (5-10 minutes)

Render va:
- Télécharger ton code
- Builder l'image Docker
- Démarrer l'application

Tu verras les logs en temps réel.

### 6. Obtenir ton URL

Une fois déployé, tu auras une URL comme:
```
https://delta-boran.onrender.com
```

### 7. Accéder depuis ton téléphone

1. Ouvre l'URL sur ton téléphone
2. **Android**: Menu → "Ajouter à l'écran d'accueil"
3. **iOS**: Partager → "Sur l'écran d'accueil"

🎉 **C'est tout!**

---

## ⚠️ Important: Mise en veille

Sur le plan gratuit, l'app s'endort après 15 minutes d'inactivité.

**Quand tu l'ouvres:**
- Premier chargement: ~30 secondes (réveil)
- Ensuite: instantané

**Pour éviter la mise en veille** (optionnel):
- Upgrade vers le plan payant ($7/mois)
- Ou utilise un service de "ping" gratuit comme UptimeRobot

---

## 🔄 Mettre à jour l'app

Après avoir modifié le code:

1. Commit et push sur GitHub:
```bash
git add .
git commit -m "Update"
git push
```

2. Render redéploie automatiquement!

---

## 📊 Voir les logs

Sur Render.com:
1. Va dans ton service
2. Onglet "Logs"
3. Logs en temps réel

---

## ❓ Problèmes courants

### Build échoue
- Vérifie que tous les fichiers sont bien sur GitHub
- Vérifie les logs de build sur Render

### App ne démarre pas
- Vérifie les variables d'environnement
- Vérifie les logs

### Connexion WebSocket échoue
- Vérifie que le CORS est bien configuré (déjà fait)
- Attends 30 secondes si l'app était endormie

---

## 💰 Plan Gratuit Render.com

**Inclus gratuitement:**
- ✅ 750 heures/mois (suffisant pour usage personnel)
- ✅ SSL/HTTPS automatique
- ✅ Déploiements illimités
- ✅ Pas de carte bancaire

**Limites:**
- ⚠️ Mise en veille après 15min d'inactivité
- ⚠️ 512MB RAM
- ⚠️ CPU partagé

---

**Besoin d'aide?** Consulte la doc Render: https://render.com/docs
