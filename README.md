# 🧠 D.E.L.T.A V2 — Design Expert Learning Technology Assistant

**DELTA** est un assistant IA vocal qui tourne **localement sur Windows** et permet de contrôler un ordinateur par la voix.

Il utilise **Google Gemini 2.5 Flash (audio natif en streaming)** pour comprendre la parole en temps réel et agir comme un assistant personnel capable de :

* ouvrir des applications
* contrôler souris et clavier
* naviguer sur le web
* exécuter du code
* gérer des projets

L’interface est une application **desktop Electron + React**, connectée à un backend **Python (FastAPI + Socket.IO)**.

---

# ⚙️ Stack technique

| Couche      | Technologie                                |
| ----------- | ------------------------------------------ |
| IA / Voix   | Google Gemini 2.5 Flash Native Audio       |
| Backend     | Python, FastAPI, Socket.IO (uvicorn)       |
| Frontend    | React 18, Vite, TailwindCSS, Framer Motion |
| Desktop     | Electron                                   |
| Vision      | MediaPipe                                  |
| TTS         | Edge TTS / Kokoro / pyttsx3                |
| Contrôle PC | PyAutoGUI, psutil, subprocess              |
| Web Agent   | Playwright + Gemini Vision                 |

---

# 📦 Prérequis

* Windows 10 ou 11
* Python **3.10+**
* Node.js **18+**
* Une clé API Gemini
* Un microphone fonctionnel

Créer une clé API ici :

https://aistudio.google.com/app/apikey

---

# 🚀 Installation

### 1 — Cloner le projet

```bash
git clone https://github.com/ton-user/delta-v2.git
cd delta-v2
```

---

### 2 — Configurer la clé API

```bash
cp .env.example .env
```

Modifier ensuite `.env` :

```
GEMINI_API_KEY=ta_cle_api
```

---

### 3 — Installer les dépendances Python

```bash
pip install -r requirements.txt
playwright install chromium
```

---

### 4 — Installer les dépendances Node

```bash
npm install
```

---

### 5 — Lancer DELTA

Méthode rapide :

```bash
lancer_delta.bat
```

Ou manuellement :

Backend :

```bash
cd backend
python server.py
```

Frontend :

```bash
npm run dev
```

---

# 🗂 Structure du projet

```
delta_v2/
├── backend/
│   ├── server.py
│   ├── ada.py
│   ├── intent_analyzer.py
│   ├── voice_commander.py
│   ├── pc_control.py
│   ├── web_agent.py
│   └── settings.json
│
├── src/
│   ├── App.jsx
│   └── components/
│
├── electron/
│   └── main.js
│
├── projects/
├── backups/
├── public/
├── lancer_delta.bat
└── requirements.txt
```

---

# 🎤 Fonctionnalités

## Voix et conversation

* conversation vocale en temps réel
* transcription en streaming
* synthèse vocale
* interaction via interface chat

---

## Contrôle du PC

DELTA peut :

* ouvrir certaines applications
* fermer des applications
* contrôler la souris
* taper du texte
* utiliser des raccourcis clavier
* exécuter certaines commandes système

⚠️ **Le contrôle du PC est encore expérimental.**
Certaines actions peuvent ne pas fonctionner correctement selon les applications ou la configuration Windows.

---

## Web Agent

DELTA peut naviguer automatiquement sur internet :

* ouvrir des pages
* cliquer
* remplir des champs
* analyser des pages avec Gemini Vision

---

## Mode Open Interpreter

Permet à DELTA de :

* installer des logiciels
* créer et modifier des fichiers
* exécuter du code Python
* analyser l’écran

---

# ⚠️ Limitations actuelles

Certaines fonctionnalités sont encore **en développement ou partiellement fonctionnelles**.

### Self-Coding Agent

Le système d’auto-codage est **expérimental**.

DELTA peut générer du code et proposer des modifications, mais **les modifications ne sont pas encore intégrées automatiquement dans son propre code source**.

Le système sert actuellement surtout à **générer ou suggérer du code**, pas à modifier directement le programme.

---

### Contrôle du PC

Le contrôle du système (souris, clavier, ouverture d’applications) **n’est pas encore parfaitement fiable**.

Certaines applications peuvent :

* ne pas être détectées
* ne pas s’ouvrir correctement
* ignorer certaines commandes.

---

### Authentification faciale

La fonctionnalité **d’authentification par reconnaissance faciale n’est plus utilisée dans cette version** du projet.

Le système a été retiré mais certaines références peuvent encore apparaître dans le code.

---

# 🧩 Fonctionnalités prévues

Fonctionnalités prévues pour les prochaines versions :

* mémoire persistante (historique intelligent)
* support multi-langues
* système de plugins
* interface web accessible sur le réseau local
* support de modèles IA locaux
* amélioration du contrôle du PC
* architecture d’agents spécialisés

---

# 🔧 Configuration

### `.env`

```
GEMINI_API_KEY=ta_cle_api_gemini
```

---

# 🧪 API Backend

Le backend expose une API REST locale :

```
http://localhost:8000
```

Exemples d’endpoints :

| Route            | Description            |
| ---------------- | ---------------------- |
| `/status`        | statut du serveur      |
| `/pc/open`       | ouvrir une application |
| `/pc/close`      | fermer une application |
| `/pc/type`       | écrire du texte        |
| `/pc/hotkey`     | raccourci clavier      |
| `/pc/screenshot` | capture d’écran        |

---

# 🧑‍💻 Créateur

**Boran Sezer**
Projet personnel — 2026
