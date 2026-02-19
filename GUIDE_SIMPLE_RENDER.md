# 📱 Guide Ultra-Simple: DELTA sur Render.com

## 🎯 En 3 étapes simples (10 minutes)

---

## ÉTAPE 1: Mettre ton code sur GitHub (5 min)

### Option la plus simple: GitHub Desktop

1. **Télécharge GitHub Desktop**: https://desktop.github.com/
2. **Installe et ouvre** GitHub Desktop
3. **Connecte-toi** avec ton compte GitHub (ou crée-en un)
4. **Ajoute ton projet**:
   - File → Add Local Repository
   - Choisis le dossier: `C:\Users\Boran\OneDrive\Bureau\DELTA_V1\delta_v2`
   - Clique "Add Repository"
5. **Publie sur GitHub**:
   - Clique sur "Publish repository" (en haut)
   - Nom: `delta-assistant`
   - Décoche "Keep this code private" (ou laisse coché si tu veux)
   - Clique "Publish repository"

✅ **Ton code est maintenant sur GitHub!**

---

## ÉTAPE 2: Créer un compte Render.com (2 min)

1. Va sur: https://render.com/
2. Clique sur "Get Started for Free"
3. Clique sur "Sign in with GitHub"
4. Autorise Render à accéder à GitHub

✅ **Ton compte Render est créé!**

---

## ÉTAPE 3: Déployer DELTA (3 min)

1. **Sur Render.com**, clique sur "New +" (en haut à droite)
2. Choisis **"Web Service"**
3. **Connecte ton repository**:
   - Clique "Connect" à côté de `delta-assistant`
4. **Configure** (laisse tout par défaut sauf):
   - Name: `delta-boran`
   - Region: Frankfurt
   - Branch: main
   - **Plan: FREE** ← Important!
5. **Scroll vers le bas** et clique sur "Advanced"
6. **Ajoute tes clés Gemini**:
   - Clique "Add Environment Variable"
   - Key: `GEMINI_API_KEY_1`
   - Value: `AIzaSyA0ZzazzoiSFya2BNxLkMVEE6YkctCKq3I`
   - Clique "Add Environment Variable" encore
   - Key: `GEMINI_API_KEY_2`
   - Value: `AIzaSyBDS0JeW9W8QOFXdbPYqlSam-0sJntyNA4`
7. **Clique sur "Create Web Service"** (en bas)

⏳ **Attends 5-10 minutes** pendant que Render déploie ton app.

Tu verras les logs défiler. Quand tu vois "Application startup complete", c'est prêt!

---

## ÉTAPE 4: Accéder depuis ton téléphone! 🎉

1. **Sur Render**, copie ton URL (en haut): `https://delta-boran.onrender.com`
2. **Sur ton téléphone**, ouvre cette URL dans Chrome/Safari
3. **Installe comme app**:
   - **Android**: Menu (3 points) → "Ajouter à l'écran d'accueil"
   - **iPhone**: Bouton Partager → "Sur l'écran d'accueil"

🎉 **DELTA est maintenant sur ton téléphone!**

---

## ⚠️ À savoir

- L'app s'endort après 15 minutes sans utilisation
- Quand tu l'ouvres, elle met ~30 secondes à se réveiller
- Ensuite, elle fonctionne normalement!

---

## 🆘 Besoin d'aide?

Si tu bloques quelque part, dis-moi à quelle étape et je t'aide!
