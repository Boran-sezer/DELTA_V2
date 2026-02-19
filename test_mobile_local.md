# 📱 Tester DELTA sur Mobile (Local)

Avant de déployer sur Fly.io, tu peux tester l'interface mobile localement.

## Étape 1: Trouver ton IP local

```powershell
ipconfig
```

Cherche "Adresse IPv4" (ex: `192.168.1.100`)

## Étape 2: Lancer DELTA

Les processus sont déjà lancés, mais assure-toi que le serveur écoute sur `0.0.0.0`:

Le fichier `server.py` a déjà été modifié pour accepter les connexions externes.

## Étape 3: Accéder depuis ton téléphone

1. Connecte ton téléphone au **même WiFi** que ton PC
2. Ouvre le navigateur sur ton téléphone
3. Va sur: `http://TON_IP:8000` (remplace TON_IP par ton adresse IPv4)

Exemple: `http://192.168.1.100:8000`

## Étape 4: Tester l'interface mobile

- ✅ Les boutons sont-ils assez grands?
- ✅ Le layout s'adapte-t-il bien?
- ✅ Le touch fonctionne-t-il correctement?
- ✅ La caméra fonctionne-t-elle?
- ✅ Le micro fonctionne-t-il?

## Problèmes courants

### "Impossible de se connecter"
- Vérifie que ton téléphone est sur le même WiFi
- Vérifie que le pare-feu Windows autorise le port 8000
- Essaie de désactiver temporairement le pare-feu

### "Caméra/Micro ne fonctionne pas"
- Les navigateurs mobiles nécessitent HTTPS pour accéder à la caméra/micro
- En local, ça ne fonctionnera pas
- Ça fonctionnera après déploiement sur Fly.io (HTTPS automatique)

## Prêt pour le cloud?

Si l'interface te plaît, déploie sur Fly.io:

```powershell
.\deploy.ps1
```

Ou suis le guide: `QUICKSTART_CLOUD.md`
