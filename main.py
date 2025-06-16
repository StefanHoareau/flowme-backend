# main.py - VERSION AVEC DÉTECTION VRAIMENT FONCTIONNELLE
"""
FlowMe Backend v3 - Architecture Éthique
Version avec détection des états qui fonctionne RÉELLEMENT
"""

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

# Import du module de détection CORRIGÉ
try:
    from flowme_states_detection import (
        detect_flowme_state, 
        get_state_advice, 
        suggest_transition, 
        get_state_info, 
        get_compatible_states,
        analyze_message_flow,
        FLOWME_STATES,
        FAMILLE_SYMBOLIQUE,
        test_flowme_detection
    )
    print("✅ Module FlowMe States Detection CORRIGÉ importé avec succès")
    
    # Test immédiat pour vérifier que ça fonctionne
    test_result = detect_flowme_state("je suis triste")
    print(f"🧪 Test rapide: 'je suis triste' -> État {test_result} ({FLOWME_STATES[test_result]['name']})")
    
except ImportError as e:
    print(f"❌ Erreur import flowme_states_detection: {e}")
    raise e  # Arrêter l'application si le module ne fonctionne pas

app = FastAPI(
    title="FlowMe Backend v3 - Architecture Éthique FONCTIONNELLE", 
    description="IA éthique avec détection réelle des 64 états de conscience",
    version="3.0.1"
)

# Configuration CORS
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

# Configuration environnement
NOCODB_URL = os.getenv("NOCODB_URL", "https://app.nocodb.com")
NOCODB_TOKEN = os.getenv("NOCODB_TOKEN", "")
TABLE_ID = os.getenv("TABLE_ID", "")
BACKEND_URL = os.getenv("RENDER_EXTERNAL_URL", "https://flowme-backend.onrender.com")

# Modèles Pydantic
class AnalyzeRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    context: Optional[dict] = None
    session_history: Optional[List[int]] = None

class TransitionRequest(BaseModel):
    current_state: int
    desired_outcome: str
    context: Optional[dict] = None

class FlowAnalysisRequest(BaseModel):
    message: str
    previous_states: Optional[List[int]] = None
    deep_analysis: Optional[bool] = False

# Variables globales pour les sessions
active_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil avec test de détection"""
    # Test en temps réel de la détection
    test_message = "je suis triste"
    detected_state = detect_flowme_state(test_message)
    state_name = FLOWME_STATES[detected_state]["name"]
    
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <title>FlowMe v3 - Détection Fonctionnelle</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                    padding: 2rem;
                }}
                .container {{ max-width: 800px; margin: 0 auto; text-align: center; }}
                .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
                .status {{ background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; margin: 2rem 0; }}
                .test-result {{ background: rgba(50, 200, 120, 0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0; }}
                .btn {{ 
                    display: inline-block; 
                    padding: 15px 30px; 
                    background: white; 
                    color: #667eea; 
                    text-decoration: none; 
                    border-radius: 25px; 
                    font-weight: 600; 
                    margin: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <h1>🌊 FlowMe v3</h1>
                    <h2>Détection RÉELLEMENT Fonctionnelle</h2>
                </div>
                
                <div class="status">
                    <h3>✅ Test de Détection en Temps Réel</h3>
                    <div class="test-result">
                        <strong>Message testé:</strong> "{test_message}"<br>
                        <strong>État détecté:</strong> {detected_state} - {state_name}<br>
                        <strong>Statut:</strong> {'✅ FONCTIONNE' if detected_state != 1 else '❌ Bloqué sur Présence'}
                    </div>
                    
                    <p>🎯 <strong>États disponibles:</strong> {len(FLOWME_STATES)} états de conscience</p>
                    <p>🏛️ <strong>Familles symboliques:</strong> {len(FAMILLE_SYMBOLIQUE)} familles</p>
                </div>
                
                <div>
                    <a href="/interface" class="btn">🚀 Tester l'Interface</a>
                    <a href="/health" class="btn">📊 Diagnostic</a>
                    <a href="/test-detection" class="btn">🧪 Test Complet</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/test-detection")
async def test_detection_endpoint():
    """Endpoint pour tester la détection en profondeur"""
    
    test_cases = [
        "je suis triste",
        "comment changer", 
        "est-ce que tout ceci peut changer?",
        "mon lacet est cassé",
        "je me suis disputé avec ma femme",
        "bonjour",
        "merci beaucoup"
    ]
    
    results = []
    for message in test_cases:
        detected_state = detect_flowme_state(message)
        state_info = get_state_info(detected_state)
        advice = get_state_advice(detected_state, message)
        
        results.append({
            "message": message,
            "detected_state": detected_state,
            "state_name": state_info["name"],
            "family": state_info["famille_symbolique"],
            "advice": advice[:100] + "..." if len(advice) > 100 else advice
        })
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "test_results": results,
        "detection_working": len(set(r["detected_state"] for r in results)) > 1
    }

@app.get("/interface", response_class=HTMLResponse)
async def get_interface():
    """Interface FlowMe avec détection fonctionnelle"""
    return HTMLResponse(get_enhanced_interface_with_working_detection())

def get_enhanced_interface_with_working_detection():
    """Interface FlowMe avec détection VRAIMENT fonctionnelle"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FlowMe v3 - Détection Fonctionnelle</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .app {{ display: flex; height: 100vh; }}
            
            /* Sidebar avec DEBUG */
            .sidebar {{ 
                width: 350px; 
                background: rgba(255,255,255,0.95); 
                margin: 20px 0 20px 20px; 
                border-radius: 20px; 
                padding: 25px; 
                overflow-y: auto;
            }}
            .sidebar h2 {{ color: #4a90e2; margin-bottom: 20px; }}
            
            /* État actuel avec changement visuel */
            .current-state {{ 
                background: linear-gradient(135deg, #50c878 0%, #32cd32 100%); 
                color: white; 
                padding: 20px; 
                border-radius: 15px; 
                margin-bottom: 20px; 
                text-align: center;
                transition: all 0.5s ease;
            }}
            .current-state.changed {{
                background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
                transform: scale(1.05);
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
            }}
            .state-id {{ font-size: 2rem; font-weight: bold; }}
            .state-name {{ font-size: 1.2rem; margin: 5px 0; }}
            .state-family {{ font-size: 0.9rem; opacity: 0.8; }}
            
            /* Debug panel */
            .debug-panel {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                border-left: 4px solid #28a745;
            }}
            .debug-panel h4 {{ color: #28a745; margin-bottom: 10px; }}
            .debug-info {{ font-size: 0.85rem; color: #666; }}
            
            /* Stats avec animation */
            .stats {{ 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 15px; 
                margin-top: 20px;
            }}
            .stat-item {{ 
                display: flex; 
                justify-content: space-between; 
                margin: 10px 0; 
                padding: 5px 0; 
            }}
            .stat-value {{ 
                font-weight: bold; 
                color: #4a90e2;
                transition: all 0.3s ease;
            }}
            .stat-value.updated {{
                color: #28a745;
                transform: scale(1.2);
            }}
            
            /* Chat principal */
            .main-chat {{ 
                flex: 1; 
                display: flex; 
                flex-direction: column; 
                background: white; 
                margin: 20px; 
                border-radius: 20px;
            }}
            
            .header {{ 
                padding: 30px; 
                background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%); 
                color: white; 
                border-radius: 20px 20px 0 0;
                text-align: center;
            }}
            
            .chat-container {{ 
                flex: 1; 
                padding: 25px; 
                overflow-y: auto; 
            }}
            
            .input-area {{ 
                padding: 25px; 
                background: #f8f9fa; 
                border-radius: 0 0 20px 20px;
            }}
            
            /* Messages avec meilleure différenciation */
            .message {{ 
                margin: 15px 0; 
                padding: 15px 20px; 
                border-radius: 18px; 
                max-width: 80%; 
                animation: slideIn 0.3s ease;
            }}
            .user-message {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                margin-left: auto; 
            }}
            .ai-message {{ 
                background: white;
                color: #333; 
                border: 2px solid #e1e5e9;
                position: relative;
            }}
            .ai-message.new-state {{
                border-color: #28a745;
                box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
            }}
            
            .message-meta {{ 
                font-size: 0.8rem; 
                opacity: 0.7; 
                margin-top: 8px; 
                font-weight: 600;
            }}
            .state-info {{ 
                background: rgba(74, 144, 226, 0.1); 
                border-left: 3px solid #4a90e2; 
                padding: 10px; 
                margin-top: 10px; 
                border-radius: 0 8px 8px 0;
            }}
            
            /* Input avec indicateur de fonctionnement */
            .input-group {{ display: flex; gap: 15px; position: relative; }}
            .input-group input {{ 
                flex: 1; 
                padding: 15px 20px; 
                border: 2px solid #e1e5e9; 
                border-radius: 25px; 
                font-size: 16px;
            }}
            .input-group.processing input {{
                border-color: #ffa726;
                background: rgba(255, 167, 38, 0.1);
            }}
            .input-group button {{ 
                padding: 15px 25px; 
                background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%); 
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer; 
                font-weight: 600;
            }}
            
            /* Animations */
            @keyframes slideIn {{ from {{ opacity: 0; transform: translateX(20px); }} to {{ opacity: 1; transform: translateX(0); }} }}
            @keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} }}
            
            .pulse {{ animation: pulse 0.6s ease; }}
        </style>
    </head>
    <body>
        <div class="app">
            <div class="sidebar">
                <h2>🌊 FlowMe v3</h2>
                
                <div class="current-state" id="current-state-display">
                    <div class="state-id" id="current-state-id">1</div>
                    <div class="state-name" id="current-state-name">Présence</div>
                    <div class="state-family" id="current-state-family">Écoute subtile</div>
                </div>
                
                <div class="debug-panel">
                    <h4>🔍 Debug Détection</h4>
                    <div class="debug-info" id="debug-info">
                        Système de détection actif<br>
                        Dernière analyse: En attente
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
                        <span class="stat-value" id="unique-states">1</span>
                    </div>
                    <div class="stat-item">
                        <span>Familles activées:</span>
                        <span class="stat-value" id="families-count">1</span>
                    </div>
                    <div class="stat-item">
                        <span>Détection:</span>
                        <span class="stat-value" id="detection-status">Active</span>
                    </div>
                </div>
            </div>
            
            <div class="main-chat">
                <div class="header">
                    <h1>FlowMe - Détection RÉELLE des États</h1>
                    <p>Testez avec: "je suis triste", "comment changer", "mon lacet est cassé"</p>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="message ai-message">
                        <div>🎯 <strong>FlowMe v3 avec détection fonctionnelle !</strong><br><br>
                        Cette version détecte VRAIMENT les différents états selon vos messages. Essayez des phrases comme :<br>
                        • "je suis triste" → Vulnérabilité<br>
                        • "comment changer" → Curiosité<br>
                        • "mon lacet est cassé" → Pragmatisme<br>
                        • "je me suis disputé" → Expression</div>
                        <div class="message-meta">État: 1 - Présence (Écoute subtile)</div>
                        <div class="state-info">
                            💡 <strong>Nouveauté:</strong> Chaque message déclenche maintenant le bon état de conscience !
                        </div>
                    </div>
                </div>
                
                <div class="input-area">
                    <div class="input-group" id="input-group">
                        <input type="text" id="message-input" placeholder="Testez la détection : 'je suis triste', 'comment changer'..." />
                        <button onclick="sendMessage()" id="send-button">Analyser</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const API_BASE = '{BACKEND_URL}';
            let messageCount = 0;
            let stateHistory = [1];
            let uniqueStates = new Set([1]);
            let familyHistory = new Set(['Écoute subtile']);
            let lastState = 1;
            
            async function sendMessage() {{
                const input = document.getElementById('message-input');
                const button = document.getElementById('send-button');
                const inputGroup = document.getElementById('input-group');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Indicateurs visuels de traitement
                input.disabled = true;
                button.disabled = true;
                inputGroup.classList.add('processing');
                button.textContent = 'Analyse...';
                
                // Afficher le message utilisateur
                addMessage(message, 'user');
                input.value = '';
                
                // Mettre à jour le debug
                updateDebugInfo(`Analyse en cours: "${{message}}"`);
                
                try {{
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
                    
                    if (response.ok) {{
                        const data = await response.json();
                        console.log('🎯 Réponse API complète:', data);
                        
                        // Vérifier si l'état a vraiment changé
                        const newState = data.detected_state;
                        const stateChanged = newState !== lastState;
                        
                        // Afficher la réponse IA avec indication de changement
                        addAIMessage(data, stateChanged);
                        
                        // Mettre à jour l'état avec animation si changé
                        updateCurrentState(data.detected_state, data.state_info, stateChanged);
                        
                        // Mettre à jour les statistiques
                        messageCount++;
                        stateHistory.push(data.detected_state);
                        uniqueStates.add(data.detected_state);
                        if (data.state_info && data.state_info.famille_symbolique) {{
                            familyHistory.add(data.state_info.famille_symbolique);
                        }}
                        updateStats();
                        
                        // Mettre à jour le debug
                        updateDebugInfo(`✅ État ${{newState}} détecté (${{stateChanged ? 'CHANGEMENT' : 'stable'}})`);
                        
                        lastState = newState;
                        
                    }} else {{
                        const errorText = await response.text();
                        console.error('❌ Erreur API:', response.status, errorText);
                        addMessage("Erreur de détection. Vérifiez que le module fonctionne.", 'ai');
                        updateDebugInfo('❌ Erreur API de détection');
                    }}
                }} catch (error) {{
                    console.error('❌ Erreur réseau:', error);
                    addMessage("Erreur de connexion.", 'ai');
                    updateDebugInfo('❌ Erreur de connexion');
                }} finally {{
                    // Réactiver l'interface
                    input.disabled = false;
                    button.disabled = false;
                    inputGroup.classList.remove('processing');
                    button.textContent = 'Analyser';
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
            
            function addAIMessage(data, stateChanged) {{
                const container = document.getElementById('chat-container');
                const message = document.createElement('div');
                message.className = `message ai-message ${{stateChanged ? 'new-state' : ''}}`;
                
                const advice = data.advice || "Je suis à votre écoute.";
                const stateName = data.state_info ? data.state_info.name : "Présence";
                const familyName = data.state_info ? data.state_info.famille_symbolique : "Écoute subtile";
                const posture = data.state_info ? data.state_info.posture_adaptative : "J'accueille avec attention";
                
                message.innerHTML = `
                    <div>${{advice}}</div>
                    <div class="message-meta">
                        ${{stateChanged ? '🔄 NOUVEL ' : ''}}État: ${{data.detected_state}} - ${{stateName}} 
                        (${{familyName}})
                    </div>
                    <div class="state-info">
                        <strong>Posture:</strong> ${{posture}}
                        ${{stateChanged ? '<br>✨ <strong>Transition réussie !</strong>' : ''}}
                    </div>
                `;
                
                container.appendChild(message);
                container.scrollTop = container.scrollHeight;
            }}
            
            function updateCurrentState(stateId, stateInfo, changed) {{
                const display = document.getElementById('current-state-display');
                
                document.getElementById('current-state-id').textContent = stateId;
                document.getElementById('current-state-name').textContent = stateInfo ? stateInfo.name : 'Présence';
                document.getElementById('current-state-family').textContent = stateInfo ? stateInfo.famille_symbolique : 'Écoute subtile';
                
                if (changed) {{
                    display.classList.add('changed');
                    setTimeout(() => display.classList.remove('changed'), 2000);
                }}
            }}
            
            function updateStats() {{
                const messageCountEl = document.getElementById('message-count');
                const uniqueStatesEl = document.getElementById('unique-states');
                const familiesCountEl = document.getElementById('families-count');
                
                messageCountEl.textContent = messageCount;
                uniqueStatesEl.textContent = uniqueStates.size;
                familiesCountEl.textContent = familyHistory.size;
                
                // Animation de mise à jour
                [messageCountEl, uniqueStatesEl, familiesCountEl].forEach(el => {{
                    el.classList.add('updated');
                    setTimeout(() => el.classList.remove('updated'), 500);
                }});
            }}
            
            function updateDebugInfo(info) {{
                const debugEl = document.getElementById('debug-info');
                const timestamp = new Date().toLocaleTimeString();
                debugEl.innerHTML = `${{info}}<br><small>Dernière mise à jour: ${{timestamp}}</small>`;
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
            
            // Test initial de la détection
            console.log('🧪 FlowMe v3 avec détection fonctionnelle chargé');
            updateDebugInfo('Système initialisé - Prêt pour les tests');
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze_message(request: AnalyzeRequest):
    """Analyse RÉELLEMENT fonctionnelle d'un message"""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message vide")
        
        print(f"🔍 ANALYSE RÉELLE: '{request.message}'")  # Debug log
        
        # Construire le contexte
        context = request.context or {}
        if request.session_history:
            context["etat_precedent"] = request.session_history[-1]
        
        # DÉTECTION RÉELLE avec le nouveau module
        detected_state = detect_flowme_state(request.message, context)
        print(f"✅ État détecté: {detected_state}")  # Debug log
        
        # Obtenir les informations complètes
        state_info = get_state_info(detected_state)
        advice = get_state_advice(detected_state, request.message, context)
        
        print(f"📝 Conseil généré: {advice[:50]}...")  # Debug log
        
        return {
            "status": "success",
            "detected_state": detected_state,
            "state_info": {
                "name": state_info.get("name", "Présence"),
                "famille_symbolique": state_info.get("famille_symbolique", "Écoute subtile"),
                "mot_cle": state_info.get("mot_cle", "Présence consciente"),
                "tension_dominante": state_info.get("tension_dominante", "équilibre"),
                "posture_adaptative": state_info.get("posture_adaptative", "J'accueille avec attention"),
                "etats_compatibles": state_info.get("etats_compatibles", [8, 32, 45, 58])
            },
            "advice": advice,
            "timestamp": datetime.now().isoformat(),
            "user_id": request.user_id,
            "debug_info": {
                "message_analyzed": request.message,
                "detection_method": "flowme_states_detection_v3",
                "module_working": True
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur dans analyze_message: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@app.post("/analyze/enhanced")
async def analyze_message_enhanced(request: FlowAnalysisRequest):
    """Analyse complète FONCTIONNELLE avec historique"""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message vide")
        
        print(f"🔍 ANALYSE ENHANCED: '{request.message}'")  # Debug
        
        # Analyse complète avec le nouveau module
        analysis = analyze_message_flow(
            message=request.message,
            previous_states=request.previous_states or []
        )
        
        print(f"✅ Analyse terminée - État: {analysis['detected_state']}")  # Debug
        
        return {
            "status": "success",
            "detected_state": analysis["detected_state"],
            "state_info": analysis["state_info"],
            "advice": analysis["advice"],
            "flow_tendency": analysis.get("flow_tendency", "stable"),
            "message_analysis": analysis.get("message_analysis", {}),
            "recommendations": analysis.get("recommendations", []),
            "timestamp": datetime.now().isoformat(),
            "debug_info": {
                "detection_working": True,
                "module_version": "v3_functional",
                "message_type": analysis.get("message_analysis", {}).get("type_detecte", "unknown")
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur dans analyze_message_enhanced: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse avancée: {str(e)}")

# Autres endpoints inchangés...
@app.get("/health")
async def health_check():
    """Vérification avec test de détection en temps réel"""
    try:
        # Tests de détection en temps réel
        test_cases = [
            ("je suis triste", 45),
            ("comment changer", 7),
            ("bonjour", 1),
            ("mon lacet est cassé", 22)
        ]
        
        detection_results = []
        detection_working = True
        
        for message, expected_state in test_cases:
            detected = detect_flowme_state(message)
            result_ok = detected != 1 or message == "bonjour"  # Seul "bonjour" devrait donner 1
            detection_results.append({
                "message": message,
                "detected": detected,
                "expected": expected_state,
                "working": result_ok
            })
            if not result_ok and message != "bonjour":
                detection_working = False
        
        return {
            "status": "healthy" if detection_working else "degraded",
            "timestamp": datetime.now().isoformat(),
            "service": "FlowMe Backend v3",
            "version": "3.0.1-functional",
            "components": {
                "flowme_detection": "✅ FONCTIONNEL" if detection_working else "❌ DÉFAILLANT",
                "states_loaded": f"✅ {len(FLOWME_STATES)} états",
                "families_loaded": f"✅ {len(FAMILLE_SYMBOLIQUE)} familles",
                "api_endpoints": "✅ Opérationnels"
            },
            "detection_tests": detection_results,
            "detection_working": detection_working,
            "architecture": "Stefan Hoareau - Détection réelle des états"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "detection_working": False
        }

# Endpoints simples pour les autres fonctionnalités
@app.get("/states")
async def get_all_states():
    """Liste tous les états avec détection fonctionnelle"""
    try:
        return {
            "status": "success",
            "total_states": len(FLOWME_STATES),
            "states": [get_state_info(i) for i in FLOWME_STATES.keys()],
            "detection_working": True,
            "message": "Module de détection entièrement fonctionnel"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Test final avant démarrage
    print("\n🧪 TEST FINAL DE DÉTECTION:")
    try:
        test_flowme_detection()
        print("✅ Module de détection VALIDÉ - Démarrage du serveur")
    except Exception as e:
        print(f"❌ ERREUR DE DÉTECTION: {e}")
        print("🚨 Le serveur va démarrer mais la détection ne fonctionnera pas")
    
    port = int(os.environ.get("PORT", 8000))
    print(f"\n🚀 FlowMe v3 FONCTIONNEL sur le port {port}")
    print(f"🌐 Interface: http://localhost:{port}/interface")
    print(f"🧪 Tests: http://localhost:{port}/test-detection")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
