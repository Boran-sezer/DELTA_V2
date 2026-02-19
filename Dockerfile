# Dockerfile pour DELTA - Optimisé pour Fly.io
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt package.json package-lock.json ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer les dépendances Node.js
RUN npm ci --only=production

# Copier le code source
COPY . .

# Build du frontend
RUN npm run build

# Créer les dossiers nécessaires
RUN mkdir -p projects backend/printer_profiles

# Exposer le port
EXPOSE 8080

# Commande de démarrage
CMD ["python", "backend/server.py"]
