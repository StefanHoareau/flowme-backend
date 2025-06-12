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

# Import du module de détection des états (maintenant créé)
from flowme_states_detection import detect_flowme_state, get_state_advice, suggest_transition, get_state_info, get_compatible_states

app = FastAPI(title="FlowMe Backend v3", description="IA éthique avec 64 états de conscience")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques si le dossier existe
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Variables d'environnement pour NocoDB
NOCODB_URL = os.getenv("NOCODB_URL", "https://app.nocodb.com")
NOCODB_TOKEN = os.getenv("NOCODB_TOKEN", "")
TABLE_ID = os.getenv("TABLE_ID", "")

class AnalyzeRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class TransitionRequest(BaseModel):
    current_state: int
    desired_outcome: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil avec liens vers l'interface"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FlowMe Backend v3</title>
            <meta charset="utf-8">
            <style>
                body { 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    margin: 0;
                    color: white;
                }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { font-size: 3em; margin-bottom: 0.5em; }
                .subtitle { font-size: 1.3em; margin-bottom: 2em; opacity: 0.9; }
                .btn { 
                    display: inline-block; 
                    padding: 15px 30px; 
                    background: white; 
                    color: #667eea; 
                    text-decoration: none; 
                    border-radius: 25px; 
                    font-weight: bold; 
                    margin: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    transition: transform 0.3s ease;
                }
                .btn:hover { transform: translateY(-2px); }
                .status { 
                    background: rgba(255,255,255,0.1); 
                    border-radius: 15px; 
                    padding: 30px; 
                    margin-top: 40px;
                }
                .endpoints { text-align: left; display: inline-block; }
                .endpoint { 
                    background: rgba(255,255,255,0.1); 
                    padding: 10px 15px; 
                    margin: 5px 0; 
                    border-radius: 8px; 
                    font-family: monospace;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌊 FlowMe Backend v3</h1>
                <p class="subtitle">IA Éthique avec 64 États de Conscience</p>
                
                <a href="/interface" class="btn">🚀 Accéder à l'Interface FlowMe</a>
                <a href="/health" class="btn">📡 Vérifier le Status</a>
                
                <div class="status">
                    <h3>📊 Status: ✅ Opérationnel</h3>
                    <p>Votre backend FlowMe est actif et prêt à analyser vos messages</p>
                    
                    <h4>🔗 Endpoints API disponibles:</h4>
                    <div class="endpoints">
                        <div class="endpoint">POST /analyze - Analyse des messages et détection d'état</div>
                        <div class="endpoint">POST /transition - Suggestions de transitions d'état</div>
                        <div class="endpoint">GET /health - Vérification de santé du service</div>
                        <div class="endpoint">GET /interface - Interface utilisateur FlowMe</div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/interface", response_class=HTMLResponse)
async def get_interface():
    """Servir l'interface FlowMe ou une interface par défaut"""
    interface_path = "static/flowme_64_interface.html"
    
    # Si le fichier HTML personnalisé n'existe pas, servir une interface par défaut
    if not os.path.exists(interface_path):
        return HTMLResponse(get_default_interface(), status_code=200)
    
    try:
        with open(interface_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Remplacer l'URL de l'API par l'URL actuelle
        html_content = html_content.replace(
            "const API_BASE = 'http://localhost:8000'",
            f"const API_BASE = '{os.getenv('RENDER_EXTERNAL_URL', 'https://flowme-backend.onrender.com')}'"
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

def get_default_interface():
    """Interface FlowMe par défaut intégrée"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FlowMe v3 - Interface Intégrée</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .app { display: flex; height: 100vh; }
            .main-chat { flex: 1; display: flex; flex-direction: column; background: white; margin: 20px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
            .sidebar { width: 300px; background: rgba(255,255,255,0.95); margin: 20px 0 20px 20px; border-radius: 20px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
            .header { padding: 30px; background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%); color: white; border-radius: 20px 20px 0 0; }
            .chat-container { flex: 1; padding: 25px; overflow-y: auto; }
            .input-area { padding: 25px; background: #f8f9fa; border-radius: 0 0 20px 20px; }
            .message { margin: 15px 0; padding: 15px 20px; border-radius: 18px; max-width: 80%; }
            .user-message { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-left: auto; }
            .ai-message { background: #f1f3f4; color: #333; }
            .input-group { display: flex; gap: 15px; }
            .input-group input { flex: 1; padding: 15px 20px; border: 2px solid #e1e5e9; border-radius: 25px; font-size: 16px; }
            .input-group button { padding: 15px 25px; background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%); color: white; border: none; border-radius: 25px; cursor: pointer; font-weight: 600; }
            .state-display { background: linear-gradient(135deg, #50c878 0%, #32cd32 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center; }
            .stats { background: #f8f9fa; padding: 20px; border-radius: 15px; margin-top: 20px; }
            .stat-item { display: flex; justify-content: space-between; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="app">
            <div class="sidebar">
                <h2 style="color: #4a90e2; margin-bottom: 20px;">🌊 FlowMe v3</h2>
                
                <div class="state-display">
                    <h3>État Actuel</h3>
                    <div id="current-state">Présence Silencieuse</div>
                </div>
                
                <div class="stats">
                    <h4>📊 Statistiques</h4>
                    <div class="stat-item">
                        <span>Messages analysés:</span>
                        <span id="message-count">0</span>
                    </div>
                    <div class="stat-item">
                        <span>États explorés:</span>
                        <span id="state-count">0</span>
                    </div>
                </div>
            </div>
            
            <div class="main-chat">
                <div class="header">
                    <h1>FlowMe - IA Éthique</h1>
                    <p>64 États de Conscience Adaptative</p>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="message ai-message">
                        Bonjour ! Je suis FlowMe, votre IA éthique. Comment puis-je vous accompagner aujourd'hui ?
                    </div>
                </div>
                
                <div class="input-area">
                    <div class="input-group">
                        <input type="text" id="message-input" placeholder="Tapez votre message ici..." />
                        <button onclick="sendMessage()">Envoyer</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const API_BASE = window.location.origin;
            let messageCount = 0;
            let stateCount = 0;
            let exploredStates = new Set();
            
            async function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value.trim();
                if (!message) return;
                
                // Afficher le message utilisateur
                addMessage(message, 'user');
                input.value = '';
                
                try {
                    // Analyser le message
                    const response = await fetch(`${API_BASE}/analyze`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        
                        // Afficher la réponse
                        addMessage(data.advice, 'ai');
                        
                        // Mettre à jour l'état
                        updateState(data.state);
                        
                        // Mettre à jour les stats
                        messageCount++;
                        exploredStates.add(data.state);
                        updateStats();
                    } else {
                        addMessage("Désolé, une erreur s'est produite. Veuillez réessayer.", 'ai');
                    }
                } catch (error) {
                    addMessage("Erreur de connexion. Vérifiez votre connexion internet.", 'ai');
                }
            }
            
            function addMessage(text, type) {
                const container = document.getElementById('chat-container');
                const message = document.createElement('div');
                message.className = `message ${type}-message`;
                message.textContent = text;
                container.appendChild(message);
                container.scrollTop = container.scrollHeight;
            }
            
            function updateState(stateId) {
                const stateNames = {
                    1: "Présence Silencieuse",
                    2: "Terre Nourricière", 
                    3: "Germination",
                    4: "Sagesse Enfantine"
                };
                
                const stateName = stateNames[stateId] || `État ${stateId}`;
                document.getElementById('current-state').textContent = stateName;
            }
            
            function updateStats() {
                document.getElementById('message-count').textContent = messageCount;
                document.getElementById('state-count').textContent = exploredStates.size;
            }
            
            // Permettre l'envoi avec Entrée
            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze_message(request: AnalyzeRequest):
    """Analyser un message et détecter l'état FlowMe"""
    try:
        # Détecter l'état
        detected_state = detect_flowme_state(request.message)
        
        # Obtenir le conseil
        advice = get_state_advice(detected_state, request.message)
        
        # Obtenir les informations de l'état
        state_info = get_state_info(detected_state)
        
        # Obtenir les états compatibles
        compatible_states = get_compatible_states(detected_state)
        
        # Données de réponse
        response_data = {
            "status": "success",
            "state": detected_state,
            "state_name": state_info["name"],
            "state_description": state_info["description"],
            "advice": advice,
            "compatible_states": compatible_states,
            "message_analyzed": request.message,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85,
            "energy": state_info["energy"]
        }
        
        # Tentative de sauvegarde NocoDB (optionnelle)
        if NOCODB_TOKEN and TABLE_ID:
            try:
                await save_to_nocodb({
                    "message": request.message,
                    "detected_state": detected_state,
                    "state_name": state_info["name"],
                    "user_id": request.user_id,
                    "timestamp": response_data["timestamp"]
                })
            except Exception as db_error:
                print(f"Erreur NocoDB (non critique): {db_error}")
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@app.post("/transition")
async def suggest_state_transition(request: TransitionRequest):
    """Suggérer une transition d'état"""
    try:
        transition_data = suggest_transition(request.current_state, request.desired_outcome)
        
        return {
            "status": "success",
            "current_state": transition_data["current_state"],
            "current_name": transition_data["current_name"],
            "suggested_states": transition_data["suggested_states"],
            "suggested_names": transition_data["suggested_names"],
            "transition_path": transition_data["path"],
            "advice": transition_data["advice"],
            "timestamp": datetime.now().isoformat()
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
        "version": "3.0.0",
        "states_loaded": len(FLOWME_STATES) if 'FLOWME_STATES' in globals() else 0,
        "endpoints": ["/", "/interface", "/analyze", "/transition", "/health"]
    }

@app.get("/states")
async def get_all_states():
    """Retourner la liste de tous les états disponibles"""
    from flowme_states_detection import FLOWME_STATES
    
    states_list = []
    for state_id, state_data in FLOWME_STATES.items():
        states_list.append({
            "id": state_id,
            "name": state_data["name"],
            "description": state_data["description"],
            "energy": state_data["energy"],
            "keywords": state_data["keywords"]
        })
    
    return {
        "status": "success",
        "total_states": len(states_list),
        "states": sorted(states_list, key=lambda x: x["id"])
    }

@app.get("/states/{state_id}")
async def get_single_state(state_id: int):
    """Retourner les détails d'un état spécifique"""
    try:
        state_info = get_state_info(state_id)
        compatible = get_compatible_states(state_id)
        
        return {
            "status": "success",
            "state": state_info,
            "compatible_states": compatible,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"État {state_id} non trouvé: {str(e)}")

async def save_to_nocodb(data: Dict[str, Any]):
    """Sauvegarder les données dans NocoDB (version simplifiée)"""
    if not NOCODB_TOKEN or not TABLE_ID:
        return
        
    headers = {
        "xc-token": NOCODB_TOKEN,
        "Content-Type": "application/json"
    }
    
    url = f"{NOCODB_URL}/api/v2/tables/{TABLE_ID}/records"
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur sauvegarde NocoDB: {e}")
        # Ne pas faire échouer l'API si NocoDB est indisponible
        return None

# Import global pour vérifier que le module fonctionne
try:
    from flowme_states_detection import FLOWME_STATES
    print(f"✅ FlowMe States chargés: {len(FLOWME_STATES)} états disponibles")
except ImportError as e:
    print(f"❌ Erreur import flowme_states_detection: {e}")
    FLOWME_STATES = {}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Démarrage FlowMe Backend v3 sur le port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
