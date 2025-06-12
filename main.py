from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

# Importer votre système de détection d'états
from flowme_states_detection import detect_flowme_state, get_state_advice, suggest_transition

app = FastAPI(title="FlowMe Backend v3", description="IA éthique avec 64 états de conscience")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques (CSS, JS, images si nécessaire)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration NocoDB
NOCODB_URL = os.getenv("NOCODB_URL", "https://app.nocodb.com")
NOCODB_TOKEN = os.getenv("NOCODB_TOKEN", "votre_token_ici")
TABLE_ID = os.getenv("TABLE_ID", "votre_table_id")

class AnalyzeRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class TransitionRequest(BaseModel):
    current_state: int
    desired_outcome: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil avec lien vers l'interface"""
    return """
    <html>
        <head><title>FlowMe Backend v3</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h1 style="color: white;">🌊 FlowMe Backend v3 - Actif</h1>
            <p style="color: white; font-size: 18px;">Votre IA éthique avec 64 états de conscience</p>
            <a href="/interface" style="display: inline-block; padding: 15px 30px; background: white; color: #667eea; text-decoration: none; border-radius: 25px; font-weight: bold; margin: 20px;">
                🚀 Accéder à l'Interface FlowMe
            </a>
            <div style="margin-top: 30px; color: white;">
                <p>📡 API Status: ✅ Opérationnel</p>
                <p>🔗 Endpoints disponibles:</p>
                <ul style="list-style: none; padding: 0;">
                    <li>POST /analyze - Analyse des messages</li>
                    <li>POST /transition - Suggestions de transition</li>
                    <li>GET /health - Status de santé</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.get("/interface", response_class=HTMLResponse)
async def get_interface():
    """Servir l'interface FlowMe complète"""
    interface_path = "static/flowme_64_interface.html"
    
    if not os.path.exists(interface_path):
        return HTMLResponse("""
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>⚠️ Interface non trouvée</h1>
                <p>Le fichier <code>static/flowme_64_interface.html</code> n'existe pas.</p>
                <p>Veuillez créer le dossier <code>static/</code> et y placer votre interface.</p>
                <a href="/">← Retour à l'accueil</a>
            </body>
        </html>
        """, status_code=404)
    
    try:
        with open(interface_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # S'assurer que l'interface utilise la bonne URL du backend
        backend_url = os.getenv("BACKEND_URL", "https://flowme-backend.onrender.com")
        html_content = html_content.replace(
            "const API_BASE = 'http://localhost:8000'",
            f"const API_BASE = '{backend_url}'"
        )
        
        return HTMLResponse(html_content)
    
    except Exception as e:
        return HTMLResponse(f"""
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>❌ Erreur de chargement</h1>
                <p>Impossible de charger l'interface: {str(e)}</p>
                <a href="/">← Retour à l'accueil</a>
            </body>
        </html>
        """, status_code=500)

@app.post("/analyze")
async def analyze_message(request: AnalyzeRequest):
    """Analyser un message et détecter l'état FlowMe"""
    try:
        # Détecter l'état selon votre architecture des 64 états
        detected_state = detect_flowme_state(request.message)
        
        # Obtenir le conseil associé
        advice = get_state_advice(detected_state, request.message)
        
        # Données à sauvegarder
        analysis_data = {
            "message": request.message,
            "detected_state": detected_state,
            "advice": advice,
            "user_id": request.user_id,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85  # À calculer selon votre logique
        }
        
        # Sauvegarder dans NocoDB (si configuré)
        if NOCODB_TOKEN != "votre_token_ici":
            try:
                await save_to_nocodb(analysis_data)
            except Exception as db_error:
                print(f"Erreur NocoDB: {db_error}")
        
        return {
            "status": "success",
            "state": detected_state,
            "advice": advice,
            "message_analyzed": request.message,
            "timestamp": analysis_data["timestamp"],
            "confidence": analysis_data["confidence"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@app.post("/transition")
async def suggest_state_transition(request: TransitionRequest):
    """Suggérer une transition d'état"""
    try:
        transition_advice = suggest_transition(request.current_state, request.desired_outcome)
        
        return {
            "status": "success",
            "current_state": request.current_state,
            "suggested_states": transition_advice.get("suggested_states", []),
            "transition_path": transition_advice.get("path", ""),
            "advice": transition_advice.get("advice", "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transition: {str(e)}")

@app.get("/health")
async def health_check():
    """Vérifier la santé du service"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FlowMe Backend v3",
        "version": "3.0.0"
    }

async def save_to_nocodb(data: Dict[str, Any]):
    """Sauvegarder les données dans NocoDB"""
    if not NOCODB_TOKEN or NOCODB_TOKEN == "votre_token_ici":
        return
        
    headers = {
        "xc-token": NOCODB_TOKEN,
        "Content-Type": "application/json"
    }
    
    url = f"{NOCODB_URL}/api/v2/tables/{TABLE_ID}/records"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        response.raise_for_status()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
