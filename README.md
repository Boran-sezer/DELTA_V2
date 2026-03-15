# 🧠 D.E.L.T.A V2 — Design Expert Learning Technology Assistant

**DELTA** est un assistant IA vocal qui tourne **localement sur Windows** et permet de contrôler un ordinateur par la voix.

Il utilise **Google Gemini 2.5 Flash (audio natif en streaming)** pour comprendre la parole en temps réel et agir comme un assistant personnel capable de :

* ouvrir des applications
* contrôler souris et clavier
* naviguer sur le web
* exécuter du code
* gérer des projets
* contrôler certains appareils connectés

L’interface est une application **desktop Electron + React**, connectée à un backend **Python (FastAPI + Socket.IO)**.

---

# ⚙️ Stack technique

| Couche        | Technologie                                |
| ------------- | ------------------------------------------ |
| IA / Voix     | Google Gemini 2.5 Flash Native Audio       |
| Backend       | Python, FastAPI, Socket.IO (uvicorn)       |
| Frontend      | React 18, Vite, TailwindCSS, Framer Motion |
| Desktop       | Electron 28                                |
| Vision        | MediaPipe (hand tracking + face landmarks) |
| TTS           | Edge TTS / Kokoro-82M / pyttsx3            |
| Contrôle PC   | PyAutoGUI, psutil, subprocess              |
| Web Agent     | Playwright + Gemini Vision                 |
| CAD           | build123d                                  |
| Smart Home    | python-kasa                                |
| Impression 3D | Moonraker API                              |

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

### 2 — Configurer la clé API

```bash
cp .env.example .env
```

Puis modifier `.env` :

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

Option simple :

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
│   ├── self_coding_agent.py
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
├── .env
├── lancer_delta.bat
└── requirements.txt
```

---

# 🎤 Fonctionnalités

## Voix et conversation

* conversation vocale en temps réel
* transcription utilisateur et IA en streaming
* interruption automatique quand l'utilisateur parle
* synthèse vocale (Edge TTS ou local)

---

## Contrôle du PC

DELTA peut :

* ouvrir ou fermer des applications
* déplacer la souris
* cliquer et scroller
* taper du texte
* utiliser des raccourcis clavier
* exécuter des commandes système
* capturer l’écran

---

## Interface

* application desktop Electron
* modules déplaçables et redimensionnables
* visualiseur audio 3D
* gestion de projets
* sélection micro / haut-parleur / webcam
* horloge et statut en temps réel

---

## Web Agent

DELTA peut naviguer automatiquement sur internet :

* ouvrir des pages
* cliquer
* remplir des formulaires
* analyser des pages avec Gemini Vision

---

## Mode Open Interpreter

* installation de logiciels
* création de fichiers
* exécution de code Python
* analyse d’écran

---

## Authentification faciale

* reconnaissance faciale avec MediaPipe
* écran de verrouillage au démarrage
* configurable dans les paramètres

---

## Self-Coding Agent

DELTA peut modifier son propre code :

1. analyse la demande utilisateur
2. génère une modification
3. crée un backup
4. applique la modification

Les sauvegardes sont stockées dans `/backups`.

---

# ⚠️ Limitations actuelles

Certaines fonctionnalités sont encore expérimentales :

* détection d’applications parfois incomplète
* précision variable du hand tracking
* Web Agent bloqué par certains sites protégés
* Self-Coding Agent encore instable sur gros changements

---

# 🧩 Fonctionnalités prévues

* mémoire persistante (vector database)
* support multi-langues
* système de plugins
* interface web accessible sur réseau local
* support modèles locaux (Ollama)
* intégration CAD complète
* notifications système Windows

---

# 🔧 Configuration

### `settings.json`

```
backend/settings.json
```

Exemple :

```json
{
  "face_auth_enabled": false,
  "tool_permissions": {
    "write_file": true,
    "read_file": true,
    "run_web_agent": true
  }
}
```

---

### `.env`

```
GEMINI_API_KEY=ta_cle_api_gemini
```

---

# 🧪 API Backend

DELTA expose une API REST locale :

```
http://localhost:8000
```

| Route            | Description       |
| ---------------- | ----------------- |
| `/status`        | statut du serveur |
| `/pc/open`       | ouvrir une app    |
| `/pc/close`      | fermer une app    |
| `/pc/click`      | clic souris       |
| `/pc/type`       | écrire du texte   |
| `/pc/hotkey`     | raccourci clavier |
| `/pc/screenshot` | capture écran     |

---

# 🧑‍💻 Créateur

**Boran Sezer**
Projet personnel — 2026
