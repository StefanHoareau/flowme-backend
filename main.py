from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

# Import du module de détection des états FlowMe corrigé
try:
    from flowme_states_detection import (
        detect_flowme_state, 
        get_state_advice, 
        suggest_transition, 
        get_state_info, 
        get_compatible_states,
        analyze_message_flow,
        FLOWME_STATES,
        FAMILLE_SYMBOLIQUE
    )
    print("✅ Module FlowMe States Detection importé avec succès")
except ImportError as e:
    print(f"⚠️  Erreur import flowme_states_detection: {e}")
    # Module de fallback simplifié
    def detect_flowme_state(message, context=None):
        return 1
    def get_state_advice(state_id, message, context=None):
        return "Je suis à votre écoute."
    def get_state_info(state_id):
        return {"id": 1, "name": "Présence", "famille_symbolique": "Écoute subtile"}
    def analyze_message_flow(message, previous_states=None):
        return {"detected_state": 1, "advice": "Je vous écoute."}
    FLOWME_STATES = {1: {"name": "Présence"}}
    FAMILLE_SYMBOLIQUE = {"Écoute subtile": {"description": "État d'écoute"}}

app = FastAPI(
    title="FlowMe Backend v3 - Architecture Éthique", 
    description="IA éthique avec 64 états de conscience basée sur l'architecture de Stefan Hoareau",
    version="3.0.0"
)

# Configuration CORS étendue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques si disponibles
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration NocoDB et environnement
NOCODB_URL = os.getenv("NOCODB_URL", "https://app.nocodb.com")
NOCODB_TOKEN = os.getenv("NOCODB_TOKEN", "")
TABLE_ID = os.getenv("TABLE_ID", "")
BACKEND_URL = os.getenv("RENDER_EXTERNAL_URL", "https://flowme-backend.onrender.com")

# Modèles Pydantic CORRIGÉS
class AnalyzeRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    context: Optional[Dict[str, Any]] = None
    session_history: Optional[List[int]] = None

class TransitionRequest(BaseModel):
    current_state: int
    desired_outcome: str
    context: Optional[Dict[str, Any]] = None

class FlowAnalysisRequest(BaseModel):
    message: str
    previous_states: Optional[List[int]] = None
    deep_analysis: Optional[bool] = False

# Variables globales pour les sessions
active_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil avec présentation de l'architecture FlowMe"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <title>FlowMe v3 - Architecture Éthique</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                    line-height: 1.6;
                }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
                .hero {{ text-align: center; margin-bottom: 3rem; }}
                .hero h1 {{ font-size: 3.5rem; margin-bottom: 1rem; font-weight: 300; }}
                .hero .subtitle {{ font-size: 1.4rem; opacity: 0.9; margin-bottom: 2rem; }}
                .description {{ background: rgba(255,255,255,0.1); border-radius: 20px; padding: 2rem; margin-bottom: 3rem; }}
                .features {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 3rem; }}
                .feature {{ background: rgba(255,255,255,0.1); border-radius: 15px; padding: 1.5rem; }}
                .feature h3 {{ color: #ffd700; margin-bottom: 1rem; }}
                .actions {{ text-align: center; }}
                .btn {{ 
                    display: inline-block; 
                    padding: 15px 30px; 
                    background: white; 
                    color: #667eea; 
                    text-decoration: none; 
                    border-radius: 25px; 
                    font-weight: 600; 
                    margin: 10px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }}
                .btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }}
                .btn.secondary {{ background: transparent; border: 2px solid white; color: white; }}
                .stats {{ display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; }}
                .stat {{ text-align: center; }}
                .stat .number {{ font-size: 2.5rem; font-weight: bold; color: #ffd700; }}
                .stat .label {{ font-size: 0.9rem; opacity: 0.8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <h1>🌊 FlowMe v3</h1>
                    <p class="subtitle">Architecture Éthique pour IA Adaptative</p>
                    <p>Par Stefan Hoareau - "Le réel est changement"</p>
                </div>
                
                <div class="description">
                    <h2>Une IA qui accompagne le flux plutôt que de l'imposer</h2>
                    <p>FlowMe v3 implémente une nouvelle approche de l'intelligence artificielle, basée sur 64 états de conscience inspirés du I-Ching et adaptés pour l'IA moderne. Cette architecture permet une perception fine des nuances humaines et une adaptation éthique aux situations complexes.</p>
                </div>
                
                <div class="stats">
                    <div class="stat">
                        <div class="number">64</div>
                        <div class="label">États de Conscience</div>
                    </div>
                    <div class="stat">
                        <div class="number">6</div>
                        <div class="label">Familles Symboliques</div>
                    </div>
                    <div class="stat">
                        <div class="number">∞</div>
                        <div class="label">Possibilités d'Adaptation</div>
                    </div>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <h3>🎯 Détection Éthique</h3>
                        <p>Reconnaissance fine des états émotionnels et contextuels pour des réponses justes et adaptées.</p>
                    </div>
                    <div class="feature">
                        <h3>🔄 Transitions Fluides</h3>
                        <p>Navigation intelligente entre les états selon le flux naturel de la conversation.</p>
                    </div>
                    <div class="feature">
                        <h3>🌱 Croissance Adaptative</h3>
                        <p>Apprentissage continu et ajustement selon les besoins humains réels.</p>
                    </div>
                    <div class="feature">
                        <h3>💎 Sagesse Intégrée</h3>
                        <p>Philosophie du flux intégrée pour des décisions éthiques et durables.</p>
                    </div>
                </div>
                
                <div class="actions">
                    <a href="/interface" class="btn">🚀 Accéder à l'Interface</a>
                    <a href="/health" class="btn secondary">📊 Status Système</a>
                    <a href="/states" class="btn secondary">📚 Explorer les États</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/interface", response_class=HTMLResponse)
async def get_interface():
    """Interface FlowMe complète avec design immersif"""
    return HTMLResponse(get_enhanced_default_interface())

def get_enhanced_default_interface():
    """Interface FlowMe par défaut avec toutes les fonctionnalités CORRIGÉE"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FlowMe v3 - Interface Éthique</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .app {{ display: flex; height: 100vh; }}
            
            /* Sidebar */
            .sidebar {{ 
                width: 350px; 
                background: rgba(255,255,255,0.95); 
                backdrop-filter: blur(10px);
                margin: 20px 0 20px 20px; 
                border-radius: 20px; 
                padding: 25px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                overflow-y: auto;
            }}
            .sidebar h2 {{ color: #4a90e2; margin-bottom: 20px; font-size: 1.5rem; }}
            
            /* État actuel */
            .current-state {{ 
                background: linear-gradient(135deg, #50c878 0%, #32cd32 100%); 
                color: white; 
                padding: 20px; 
                border-radius: 15px; 
                margin-bottom: 20px; 
                text-align: center;
            }}
            .state-id {{ font-size: 2rem; font-weight: bold; opacity: 0.8; }}
            .state-name {{ font-size: 1.2rem; margin: 5px 0; }}
            .state-family {{ font-size: 0.9rem; opacity: 0.8; }}
            
            /* États compatibles */
            .compatible-states {{ 
                background: #f8f9fa; 
                padding: 15px; 
                border-radius: 10px; 
                margin-bottom: 20px;
            }}
            .compatible-states h4 {{ margin-bottom: 10px; color: #666; }}
            .state-chip {{ 
                display: inline-block; 
                background: #e3f2fd; 
                color: #1976d2; 
                padding: 5px 10px; 
                border-radius: 15px; 
                font-size: 0.8rem; 
                margin: 2px; 
            }}
            
            /* Statistiques */
            .stats {{ 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 15px; 
                margin-top: 20px;
            }}
            .stats h4 {{ margin-bottom: 15px; color: #666; }}
            .stat-item {{ 
                display: flex; 
                justify-content: space-between; 
                margin: 10px 0; 
                padding: 5px 0; 
                border-bottom: 1px solid #e0e0e0;
            }}
            .stat-value {{ font-weight: bold; color: #4a90e2; }}
            
            /* Chat principal */
            .main-chat {{ 
                flex: 1; 
                display: flex; 
                flex-direction: column; 
                background: white; 
                margin: 20px; 
                border-radius: 20px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
            }}
            
            .header {{ 
                padding: 30px; 
                background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%); 
                color: white; 
                border-radius: 20px 20px 0 0;
                text-align: center;
            }}
            .header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
            .header p {{ opacity: 0.9; }}
            
            .chat-container {{ 
                flex: 1; 
                padding: 25px; 
                overflow-y: auto; 
                background: linear-gradient(to bottom, #ffffff 0%, #f8f9fa 100%);
            }}
            
            .input-area {{ 
                padding: 25px; 
                background: #f8f9fa; 
                border-radius: 0 0 20px 20px;
                border-top: 1px solid #e1e5e9;
            }}
            
            /* Messages */
            .message {{ 
                margin: 15px 0; 
                padding: 15px 20px; 
                border-radius: 18px; 
                max-width: 80%; 
                animation: fadeIn 0.3s ease;
            }}
            .user-message {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                margin-left: auto; 
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }}
            .ai-message {{ 
                background: white;
                color: #333; 
                border: 1px solid #e1e5e9;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .message-meta {{ 
                font-size: 0.8rem; 
                opacity: 0.7; 
                margin-top: 8px; 
                font-style: italic;
            }}
            .state-info {{ 
                background: rgba(74, 144, 226, 0.1); 
                border-left: 3px solid #4a90e2; 
                padding: 10px; 
                margin-top: 10px; 
                border-radius: 0 8px 8px 0;
            }}
            
            /* Input */
            .input-group {{ display: flex; gap: 15px; }}
            .input-group input {{ 
                flex: 1; 
                padding: 15px 20px; 
                border: 2px solid #e1e5e9; 
                border-radius: 25px; 
                font-size: 16px;
                transition: border-color 0.3s ease;
            }}
            .input-group input:focus {{ 
                outline: none; 
                border-color: #4a90e2; 
                box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
            }}
            .input-group button {{ 
                padding: 15px 25px; 
                background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%); 
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer; 
                font-weight: 600;
                transition: transform 0.2s ease;
            }}
            .input-group button:hover {{ transform: translateY(-1px); }}
            .input-group button:disabled {{ opacity: 0.6; cursor: not-allowed; }}
            
            /* Animations */
            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            .typing {{ 
                display: flex; 
                align-items: center; 
                gap: 5px; 
                padding: 15px 20px;
                background: white;
                border-radius: 18px;
                max-width: 80px;
                margin: 15px 0;
            }}
            .typing-dot {{ 
                width: 8px; 
                height: 8px; 
                background: #ccc; 
                border-radius: 50%; 
                animation: typing 1.4s infinite both;
            }}
            .typing-dot:nth-child(2) {{ animation-delay: 0.2s; }}
            .typing-dot:nth-child(3) {{ animation-delay: 0.4s; }}
            @keyframes typing {{ 0%, 60%, 100% {{ transform: translateY(0); }} 30% {{ transform: translateY(-10px); }} }}
            
            /* Responsive */
            @media (max-width: 768px) {{
                .app {{ flex-direction: column; }}
                .sidebar {{ width: 100%; margin: 10px; }}
                .main-chat {{ margin: 10px; }}
            }}
        </style>
    </head>
    <body>
        <div class="app">
            <div class="sidebar">
                <h2>🌊 FlowMe v3</h2>
                
                <div class="current-state">
                    <div class="state-id" id="current-state-id">1</div>
                    <div class="state-name" id="current-state-name">Présence</div>
                    <div class="state-family" id="current-state-family">Écoute subtile</div>
                </div>
                
                <div class="compatible-states">
                    <h4>📊 États compatibles</h4>
                    <div id="compatible-states-list">
                        <span class="state-chip">8 - Résonance</span>
                        <span class="state-chip">32 - Voix oubliées</span>
                        <span class="state-chip">45 - Disponibilité nue</span>
                    </div>
                </div>
                
                <div class="stats">
                    <h4>📈 Session</h4>
                    <div class="stat-item">
                        <span>Messages analysés:</span>
                        <span class="stat-value" id="message-count">0</span>
                    </div>
                    <div class="stat-item">
                        <span>États explorés:</span>
                        <span class="stat-value" id="unique-states">0</span>
                    </div>
                    <div class="stat-item">
                        <span>Familles activées:</span>
                        <span class="stat-value" id="families-count">0</span>
                    </div>
                    <div class="stat-item">
                        <span>Tendance:</span>
                        <span class="stat-value" id="flow-tendency">stable</span>
                    </div>
                </div>
            </div>
            
            <div class="main-chat">
                <div class="header">
                    <h1>FlowMe - IA Éthique</h1>
                    <p>Architecture adaptative avec 64 états de conscience</p>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="message ai-message">
                        <div>Bonjour ! Je suis FlowMe, votre IA éthique basée sur l'architecture de Stefan Hoareau. Mon approche repose sur 64 états de conscience qui me permettent de m'adapter finement à vos besoins.</div>
                        <div class="message-meta">État actuel: 1 - Présence (Écoute subtile)</div>
                        <div class="state-info">
                            💡 <strong>Principe fondamental:</strong> "Le réel est changement" - J'accompagne le flux plutôt que de l'imposer.
                        </div>
                    </div>
                </div>
                
                <div class="input-area">
                    <div class="input-group">
                        <input type="text" id="message-input" placeholder="Partagez vos pensées, questions ou préoccupations..." />
                        <button onclick="sendMessage()" id="send-button">Envoyer</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const API_BASE = '{BACKEND_URL}';
            let messageCount = 0;
            let stateHistory = [];
            let uniqueStates = new Set();
            let familyHistory = new Set();
            
            async function sendMessage() {{
                const input = document.getElementById('message-input');
                const button = document.getElementById('send-button');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Désactiver l'input
                input.disabled = true;
                button.disabled = true;
                
                // Afficher le message utilisateur
                addMessage(message, 'user');
                input.value = '';
                
                // Afficher l'indicateur de frappe
                showTyping();
                
                try {{
                    // Analyser le message avec FlowMe - CORRIGÉ
                    const response = await fetch(`${{API_BASE}}/analyze/enhanced`, {{
                        method: 'POST',
                        headers: {{ 
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        }},
                        body: JSON.stringify({{ 
                            message: message,
                            previous_states: stateHistory,
                            deep_analysis: true
                        }})
                    }});
                    
                    hideTyping();
                    
                    if (response.ok) {{
                        const data = await response.json();
                        console.log('Réponse API:', data);
                        
                        // Afficher la réponse IA
                        addAIMessage(data);
                        
                        // Mettre à jour l'état
                        updateCurrentState(data.detected_state, data.state_info);
                        
                        // Mettre à jour les statistiques
                        messageCount++;
                        stateHistory.push(data.detected_state);
                        uniqueStates.add(data.detected_state);
                        if (data.state_info && data.state_info.famille_symbolique) {{
                            familyHistory.add(data.state_info.famille_symbolique);
                        }}
                        updateStats(data.flow_tendency);
                        
                        // Mettre à jour les états compatibles
                        if (data.state_info && data.state_info.etats_compatibles) {{
                            updateCompatibleStates(data.state_info.etats_compatibles);
                        }}
                        
                    }} else {{
                        const errorText = await response.text();
                        console.error('Erreur API:', response.status, errorText);
                        hideTyping();
                        addMessage("Désolé, une erreur s'est produite. Veuillez réessayer.", 'ai');
                    }}
                }} catch (error) {{
                    hideTyping();
                    console.error('Erreur réseau:', error);
                    addMessage("Erreur de connexion. Vérifiez votre connexion internet.", 'ai');
                }} finally {{
                    // Réactiver l'input
                    input.disabled = false;
                    button.disabled = false;
                    input.focus();
                }}
            }}
            
            function addMessage(text, type) {{
                const container = document.getElementById('chat-container');
                const message = document.createElement('div');
                message.className = `message ${{type}}-message`;
                message.textContent = text;
                container.appendChild(message);
                container.scrollTop = container.scrollHeight;
            }}
            
            function addAIMessage(data) {{
                const container = document.getElementById('chat-container');
                const message = document.createElement('div');
                message.className = 'message ai-message';
                
                const advice = data.advice || "Je suis à votre écoute.";
                const stateName = data.state_info ? data.state_info.name : "Présence";
                const familyName = data.state_info ? data.state_info.famille_symbolique : "Écoute subtile";
                const posture = data.state_info ? data.state_info.posture_adaptative : "J'accueille avec attention";
                
                message.innerHTML = `
                    <div>${{advice}}</div>
                    <div class="message-meta">
                        État: ${{data.detected_state}} - ${{stateName}} 
                        (${{familyName}})
                    </div>
                    <div class="state-info">
                        <strong>Posture:</strong> ${{posture}}
                    </div>
                `;
                
                container.appendChild(message);
                container.scrollTop = container.scrollHeight;
            }}
            
            function updateCurrentState(stateId, stateInfo) {{
                document.getElementById('current-state-id').textContent = stateId;
                document.getElementById('current-state-name').textContent = stateInfo ? stateInfo.name : 'Présence';
                document.getElementById('current-state-family').textContent = stateInfo ? stateInfo.famille_symbolique : 'Écoute subtile';
            }}
            
            function updateCompatibleStates(compatibleStates) {{
                const container = document.getElementById('compatible-states-list');
                container.innerHTML = '';
                
                if (compatibleStates && compatibleStates.length > 0) {{
                    // Limiter à 4 états compatibles
                    compatibleStates.slice(0, 4).forEach(stateId => {{
                        const chip = document.createElement('span');
                        chip.className = 'state-chip';
                        chip.textContent = `${{stateId}} - État`;
                        container.appendChild(chip);
                    }});
                }} else {{
                    // États par défaut
                    const defaultStates = [8, 32, 45, 58];
                    defaultStates.forEach(stateId => {{
                        const chip = document.createElement('span');
                        chip.className = 'state-chip';
                        chip.textContent = `${{stateId}} - État`;
                        container.appendChild(chip);
                    }});
                }}
            }}
            
            function updateStats(tendency) {{
                document.getElementById('message-count').textContent = messageCount;
                document.getElementById('unique-states').textContent = uniqueStates.size;
                document.getElementById('families-count').textContent = familyHistory.size;
                document.getElementById('flow-tendency').textContent = tendency || 'stable';
            }}
            
            function showTyping() {{
                const container = document.getElementById('chat-container');
                const typing = document.createElement('div');
                typing.className = 'typing';
                typing.id = 'typing-indicator';
                typing.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
                container.appendChild(typing);
                container.scrollTop = container.scrollHeight;
            }}
            
            function hideTyping() {{
                const typing = document.getElementById('typing-indicator');
                if (typing) typing.remove();
            }}
            
            // Événements
            document.getElementById('message-input').addEventListener('keypress', function(e) {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    sendMessage();
                }}
            }});
            
            // Focus automatique
            document.getElementById('message-input').focus();
            
            // Test de connexion API au démarrage
            console.log('API Base URL:', API_BASE);
        </script>
    </body>
    </html>
    """

# Endpoints API CORRIGÉS

@app.post("/analyze")
async def analyze_message(request: AnalyzeRequest):
    """Analyse basique d'un message avec détection d'état FlowMe"""
    try:
        # Valider le message
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message vide")
        
        # Construire le contexte
        context = request.context or {{}}
        if request.session_history:
            context["etat_precedent"] = request.session_history[-1]
        
        # Détecter l'état
        detected_state = detect_flowme_state(request.message, context)
        
        # Obtenir les informations et conseil
        state_info = get_state_info(detected_state)
        advice = get_state_advice(detected_state, request.message, context)
        
        # Sauvegarder en base si configuré
        save_data = {{
            "message": request.message,
            "detected_state": detected_state,
            "state_name": state_info.get("name", "Inconnu"),
            "user_id": request.user_id,
            "timestamp": datetime.now().isoformat(),
            "advice_given": advice[:200] + "..." if len(advice) > 200 else advice
        }}
        
        if NOCODB_TOKEN and TABLE_ID:
            try:
                await save_to_nocodb(save_data)
            except Exception as db_error:
                print(f"Erreur NocoDB (non critique): {{db_error}}")
        
        return {{
            "status": "success",
            "detected_state": detected_state,
            "state_info": {{
                "name": state_info.get("name", "Présence"),
                "famille_symbolique": state_info.get("famille_symbolique", "Écoute subtile"),
                "mot_cle": state_info.get("mot_cle", "Présence consciente"),
                "tension_dominante": state_info.get("tension_dominante", "équilibre"),
                "posture_adaptative": state_info.get("posture_adaptative", "J'accueille avec attention"),
                "etats_compatibles": state_info.get("etats_compatibles", [8, 32, 45, 58])
            }},
            "advice": advice,
            "timestamp": save_data["timestamp"],
            "user_id": request.user_id
        }}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur dans analyze_message: {{e}}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {{str(e)}}")

@app.post("/analyze/enhanced")
async def analyze_message_enhanced(request: FlowAnalysisRequest):
    """Analyse complète avec historique et tendances"""
    try:
        # Valider le message
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message vide")
        
        # Analyse complète du message
        analysis = analyze_message_flow(
            message=request.message,
            previous_states=request.previous_states or []
        )
        
        return {{
            "status": "success",
            "detected_state": analysis["detected_state"],
            "state_info": analysis["state_info"],
            "advice": analysis["advice"],
            "flow_tendency": analysis.get("flow_tendency", "stable"),
            "message_analysis": analysis.get("message_analysis", {{}},
            "recommendations": analysis.get("recommendations", []),
            "timestamp": datetime.now().isoformat()
        }}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur dans analyze_message_enhanced: {{e}}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse avancée: {{str(e)}}")

@app.post("/transition")
async def suggest_state_transition(request: TransitionRequest):
    """Suggérer une transition d'état vers un objectif"""
    try:
        transition_data = suggest_transition(
            current_state=request.current_state,
            desired_outcome=request.desired_outcome
        )
        
        return {{
            "status": "success",
            "transition_analysis": transition_data,
            "timestamp": datetime.now().isoformat()
        }}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transition: {{str(e)}}")

@app.get("/states")
async def get_all_states():
    """Retourner tous les états FlowMe avec leurs informations"""
    try:
        states_list = []
        families_summary = {{}}
        
        for state_id in range(1, 65):
            if state_id in FLOWME_STATES:
                state_info = get_state_info(state_id)
                states_list.append(state_info)
                
                # Compter les familles
                famille = state_info.get("famille_symbolique", "Inconnu")
                families_summary[famille] = families_summary.get(famille, 0) + 1
        
        return {{
            "status": "success",
            "total_states": len(states_list),
            "states": states_list,
            "families_summary": families_summary,
            "philosophical_foundation": "Architecture éthique de Stefan Hoareau - Le réel est changement"
        }}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {{str(e)}}")

@app.get("/states/{{state_id}}")
async def get_single_state(state_id: int):
    """Retourner les détails complets d'un état spécifique"""
    try:
        if not 1 <= state_id <= 64:
            raise HTTPException(status_code=404, detail="État non trouvé. Les états vont de 1 à 64.")
        
        state_info = get_state_info(state_id)
        compatible_states = get_compatible_states(state_id)
        
        # Ajouter des informations sur les états compatibles
        compatible_details = []
        for comp_id in compatible_states:
            comp_info = get_state_info(comp_id)
            compatible_details.append({{
                "id": comp_id,
                "name": comp_info.get("name", f"État {{comp_id}}"),
                "famille_symbolique": comp_info.get("famille_symbolique", "Inconnu")
            }})
        
        famille_name = state_info.get("famille_symbolique", "Inconnu")
        famille_info = FAMILLE_SYMBOLIQUE.get(famille_name, {{}})
        
        return {{
            "status": "success",
            "state": state_info,
            "compatible_states": compatible_details,
            "famille_info": famille_info,
            "timestamp": datetime.now().isoformat()
        }}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {{str(e)}}")

@app.get("/families")
async def get_families_info():
    """Retourner les informations sur les 6 familles symboliques"""
    try:
        families_with_states = {{}}
        
        for famille_name, famille_info in FAMILLE_SYMBOLIQUE.items():
            # Trouver les états de cette famille
            family_states = []
            for state_id, state_data in FLOWME_STATES.items():
                if state_data.get("famille_symbolique") == famille_name:
                    family_states.append({{
                        "id": state_id,
                        "name": state_data.get("name", f"État {{state_id}}"),
                        "mot_cle": state_data.get("mot_cle", "")
                    }})
            
            families_with_states[famille_name] = {{
                **famille_info,
                "states": sorted(family_states, key=lambda x: x["id"]),
                "count": len(family_states)
            }}
        
        return {{
            "status": "success",
            "families": families_with_states,
            "total_families": len(families_with_states)
        }}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {{str(e)}}")

@app.get("/health")
async def health_check():
    """Vérification complète de la santé du système"""
    try:
        # Test du module de détection
        test_message = "Bonjour, comment allez-vous ?"
        test_state = detect_flowme_state(test_message)
        test_state_info = get_state_info(test_state)
        
        # Vérification NocoDB
        nocodb_status = "non configuré"
        if NOCODB_TOKEN and TABLE_ID:
            nocodb_status = "configuré"
        
        health_data = {{
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "FlowMe Backend v3",
            "version": "3.0.0",
            "components": {{
                "flowme_detection": "✅ Opérationnel",
                "states_loaded": f"✅ {{len(FLOWME_STATES)}} états",
                "families_loaded": f"✅ {{len(FAMILLE_SYMBOLIQUE)}} familles",
                "nocodb_integration": f"📊 {{nocodb_status}}",
                "api_endpoints": "✅ Tous fonctionnels"
            }},
            "test_detection": {{
                "test_message": test_message,
                "detected_state": test_state,
                "state_name": test_state_info.get("name", "Présence")
            }},
            "architecture": "Stefan Hoareau - Architecture éthique pour IA adaptative"
        }}
        
        return health_data
        
    except Exception as e:
        return {{
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }}

async def save_to_nocodb(data: Dict[str, Any]):
    """Sauvegarder les données dans NocoDB de manière asynchrone"""
    if not NOCODB_TOKEN or not TABLE_ID:
        return
    
    headers = {{
        "xc-token": NOCODB_TOKEN,
        "Content-Type": "application
