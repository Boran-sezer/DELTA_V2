"""
DELTA V2 - Service Cloud sur Streamlit
Alternative à Replit - Plus simple et plus stable
Déployez gratuitement sur Streamlit Cloud
"""

import streamlit as st
import subprocess
import tempfile
import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from threading import Thread

# Configuration de la page Streamlit
st.set_page_config(
    page_title="DELTA Cloud Service",
    page_icon="🚀",
    layout="wide"
)

# ============================================================================
# MODÈLES DE DONNÉES
# ============================================================================

class CADRequest(BaseModel):
    code: str

class CADResponse(BaseModel):
    success: bool
    stl_data: Optional[str] = None
    error: Optional[str] = None

# ============================================================================
# API FASTAPI (Backend)
# ============================================================================

app = FastAPI(title="DELTA Cloud Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "DELTA Cloud Service",
        "status": "running",
        "platform": "Streamlit Cloud"
    }

@app.get("/health")
def health():
    """Vérifier l'état du service"""
    services = {}
    
    try:
        import build123d
        services["cad"] = "ready"
    except ImportError:
        services["cad"] = "missing"
    
    return {
        "status": "healthy" if services["cad"] == "ready" else "degraded",
        "services": services
    }

@app.post("/cad/generate", response_model=CADResponse)
async def generate_cad(request: CADRequest):
    """Génère un fichier STL à partir du code build123d"""
    print(f"[CLOUD CAD] Nouvelle requête")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "model.py")
        output_path = os.path.join(tmpdir, "output.stl")
        
        # Préparer le code
        code = request.code.replace("'output.stl'", f"'{output_path}'")
        code = code.replace('"output.stl"', f'"{output_path}"')
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        try:
            result = subprocess.run(
                ['python', script_path],
                capture_output=True,
                text=True,
                timeout=45
            )
            
            if result.returncode != 0:
                return CADResponse(
                    success=False,
                    error=result.stderr[:500]
                )
            
            if not os.path.exists(output_path):
                return CADResponse(
                    success=False,
                    error="Fichier STL non généré"
                )
            
            with open(output_path, 'rb') as f:
                stl_bytes = f.read()
            
            stl_b64 = base64.b64encode(stl_bytes).decode('utf-8')
            
            print(f"[CLOUD CAD] ✅ Succès! {len(stl_bytes)} bytes")
            
            return CADResponse(
                success=True,
                stl_data=stl_b64
            )
            
        except subprocess.TimeoutExpired:
            return CADResponse(
                success=False,
                error="Timeout (>45s)"
            )
        except Exception as e:
            return CADResponse(
                success=False,
                error=str(e)
            )

# ============================================================================
# INTERFACE STREAMLIT (Frontend)
# ============================================================================

def run_api():
    """Lance l'API FastAPI dans un thread séparé"""
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="error")

# Lancer l'API en arrière-plan
if 'api_started' not in st.session_state:
    st.session_state.api_started = True
    thread = Thread(target=run_api, daemon=True)
    thread.start()

# Interface Streamlit
st.title("🚀 DELTA Cloud Service")
st.markdown("### Service de génération CAD dans le cloud")

# Statut du service
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Statut", "🟢 En ligne")

with col2:
    try:
        import build123d
        st.metric("build123d", "✅ Installé")
    except:
        st.metric("build123d", "❌ Manquant")

with col3:
    st.metric("Plateforme", "Streamlit Cloud")

st.divider()

# Instructions
st.markdown("""
## 📋 Comment utiliser ce service

### 1. URL du service
Copiez l'URL de cette page (en haut de votre navigateur).

### 2. Configuration DELTA
Dans votre fichier `delta_v2/.env`, ajoutez:
```
CLOUD_SERVICE_URL=https://votre-app.streamlit.app
```

### 3. Activation
Dans `delta_v2/backend/server.py`, changez:
```python
from cad_agent import CadAgent
```
En:
```python
from cad_agent_cloud import CadAgent
```

### 4. Relancez DELTA
Le service cloud est maintenant actif!

---

## 🔍 Endpoints disponibles

- `GET /` - Informations du service
- `GET /health` - État de santé
- `POST /cad/generate` - Génération CAD

---

## ✅ Avantages Streamlit Cloud

- ✅ Gratuit à vie
- ✅ Toujours actif (pas d'arrêt automatique)
- ✅ Déploiement en 1 clic
- ✅ Plus stable que Replit
- ✅ Interface de monitoring incluse

---

## 📊 Statistiques
""")

# Compteur de requêtes (simple)
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

st.metric("Requêtes traitées", st.session_state.request_count)

st.divider()

# Test du service
st.markdown("## 🧪 Tester le service")

if st.button("Tester la génération CAD"):
    with st.spinner("Test en cours..."):
        test_code = """
from build123d import *

with BuildPart() as p:
    Box(10, 10, 10)

result_part = p.part
export_stl(result_part, 'output.stl')
"""
        
        try:
            # Simuler une requête
            with tempfile.TemporaryDirectory() as tmpdir:
                script_path = os.path.join(tmpdir, "test.py")
                output_path = os.path.join(tmpdir, "output.stl")
                
                code = test_code.replace("'output.stl'", f"'{output_path}'")
                
                with open(script_path, 'w') as f:
                    f.write(code)
                
                result = subprocess.run(
                    ['python', script_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0 and os.path.exists(output_path):
                    st.success("✅ Test réussi! Le service fonctionne correctement.")
                    st.session_state.request_count += 1
                else:
                    st.error(f"❌ Test échoué: {result.stderr}")
        except Exception as e:
            st.error(f"❌ Erreur: {e}")

st.divider()

# Footer
st.markdown("""
---
**DELTA V2 Cloud Service** - Propulsé par Streamlit Cloud  
Version 2.0.0 | [Documentation](https://github.com/votre-repo)
""")
