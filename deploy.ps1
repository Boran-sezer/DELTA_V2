# Script de déploiement automatique pour Fly.io
# Usage: .\deploy.ps1

Write-Host "🚀 Déploiement DELTA sur Fly.io" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Fly CLI est installé
if (-not (Get-Command fly -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Fly CLI n'est pas installé!" -ForegroundColor Red
    Write-Host "Installe-le avec: iwr https://fly.io/install.ps1 -useb | iex" -ForegroundColor Yellow
    exit 1
}

# Vérifier si l'utilisateur est connecté
$authStatus = fly auth whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tu n'es pas connecté à Fly.io!" -ForegroundColor Red
    Write-Host "Connecte-toi avec: fly auth login" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Connecté en tant que: $authStatus" -ForegroundColor Green
Write-Host ""

# Vérifier si l'app existe
$appExists = fly status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Première fois? Création de l'app..." -ForegroundColor Yellow
    Write-Host ""
    
    # Demander les clés Gemini
    $key1 = Read-Host "Entre ta GEMINI_API_KEY_1"
    $key2 = Read-Host "Entre ta GEMINI_API_KEY_2 (optionnel, appuie sur Entrée pour ignorer)"
    
    # Lancer l'app
    fly launch --no-deploy
    
    # Configurer les secrets
    Write-Host ""
    Write-Host "🔐 Configuration des secrets..." -ForegroundColor Cyan
    fly secrets set "GEMINI_API_KEY_1=$key1"
    
    if ($key2) {
        fly secrets set "GEMINI_API_KEY_2=$key2"
    }
}

# Déployer
Write-Host ""
Write-Host "🚀 Déploiement en cours..." -ForegroundColor Cyan
fly deploy

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Déploiement réussi!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Accède à ton app:" -ForegroundColor Cyan
    fly open
    Write-Host ""
    Write-Host "📊 Voir les logs:" -ForegroundColor Cyan
    Write-Host "   fly logs" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Déploiement échoué!" -ForegroundColor Red
    Write-Host "Consulte les logs avec: fly logs" -ForegroundColor Yellow
}
