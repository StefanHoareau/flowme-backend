# main.py - VERSION AVEC INTERFACE ÉPURÉE INTÉGRÉE
"""
FlowMe Backend v3 - Version avec interface épurée focalisée utilisateur
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

# Import sécurisé du module de détection
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
    DETECTION_WORKING = True
except ImportError as e:
    print(f"❌ Import flowme_states_detection échoué: {e}")
    # Fallbacks
    DETECTION_WORKING = False
    FLOWME_STATES = {1: {"name": "Présence", "famille_symbolique": "Écoute subtile"}}
    FAMILLE_SYMBOLIQUE = {"Écoute subtile": {"description": "États d'attention"}}
    
    def detect_flowme_state(message: str, context: Optional[Dict] = None) -> int:
        return 1
    
    def get_state_advice(state_id: int, message: str, context: Optional[Dict] = None) -> str:
        return "J'accueille avec attention totale"
    
    def get_state_info(state_id: int) -> Dict[str, Any]:
        return {"id": 1, "name": "Présence", "famille_symbolique": "Écoute subtile", "posture_adaptative": "J'accueille avec attention"}
    
    def analyze_message_flow(message: str, previous_states: Optional[List[int]] = None) -> Dict[str, Any]:
        return {"detected_state": 1, "state_info": get_state_info(1), "advice": get_state_advice(1, message), "flow_tendency": "stable", "message_analysis": {"type_detecte": "fallback"}, "recommendations": []}

app = FastAPI(
    title="FlowMe v3 - Interface Épurée", 
    description="IA éthique avec interface focalisée utilisateur",
    version="3.1.0-clean"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration environnement
BACKEND_URL = os.getenv("RENDER_EXTERNAL_URL", "https://flowme-backend.onrender.com")

# Modèles Pydantic
class AnalyzeRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    context: Optional[dict] = None
    session_history: Optional[List[int]] = None

class FlowAnalysisRequest(BaseModel):
    message: str
    previous_states: Optional[List[int]] = None
    deep_analysis: Optional[bool] = False

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil épurée"""
    status_text = "FONCTIONNELLE" if DETECTION_WORKING else "MODE DÉGRADÉ"
    status_color = "#28a745" if DETECTION_WORKING else "#ffc107"
    
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <title>FlowMe v3 - Interface Épurée</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 2rem;
                }}
                .container {{ 
                    max-width: 600px; 
                    text-align: center;
                    background: rgba(255,255,255,0.1);
                    padding: 3rem;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }}
                .logo {{ 
                    font-size: 4rem; 
                    margin-bottom: 1rem;
                    background: linear-gradient(45deg, #fff, #f0f8ff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}
                .status-badge {{
                    background: {status_color};
                    color: white;
                    padding: 8px 20px;
                    border-radius: 25px;
                    font-weight: bold;
                    display: inline-block;
                    margin: 20px 0;
                    font-size: 0.9rem;
                }}
                .description {{
                    font-size: 1.2rem;
                    margin: 20px 0;
                    opacity: 0.9;
                    line-height: 1.6;
                }}
                .cta-button {{ 
                    display: inline-block; 
                    padding: 15px 30px; 
                    background: white; 
                    color: #667eea; 
                    text-decoration: none; 
                    border-radius: 25px; 
                    font-weight: 600; 
                    margin: 20px 10px;
                    transition: transform 0.2s ease;
                }}
                .cta-button:hover {{
                    transform: translateY(-2px);
                }}
                .features {{
                    margin-top: 30px;
                    text-align: left;
                    background: rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 15px;
                }}
                .feature {{
                    margin: 10px 0;
                    display: flex;
                    align-items: center;
                }}
                .feature-icon {{
                    margin-right: 10px;
                    font-size: 1.2rem;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">🌊 FlowMe</div>
                <h1>Accompagnement Conscient</h1>
                <div class="status-badge">{status_text}</div>
                
                <div class="description">
                    Explorez vos états de conscience en dialogue authentique. 
                    FlowMe détecte et s'adapte à votre flux naturel d'expression.
                </div>
                
                <div class="features">
                    <div class="feature">
                        <span class="feature-icon">🎯</span>
                        <span>Détection de {len(FLOWME_STATES)} états de conscience</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🏛️</span>
                        <span>{len(FAMILLE_SYMBOLIQUE)} familles symboliques</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">💬</span>
                        <span>Dialogue éthique et bienveillant</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🌱</span>
                        <span>Accompagnement vers plus de conscience</span>
                    </div>
                </div>
                
                <a href="/interface" class="cta-button">🚀 Commencer le Dialogue</a>
            </div>
        </body>
    </html>
    """

@app.get("/interface", response_class=HTMLResponse)
async def get_clean_interface():
    """Interface FlowMe épurée et focalisée utilisateur"""
    return HTMLResponse(get_clean_flowme_interface())

def get_clean_flowme_interface():
    """Interface FlowMe épurée sans éléments techniques"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FlowMe - Dialogue Conscient</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            
            .app {{ display: flex; height: 100vh; }}
            
            .sidebar {{
                width: 280px;
                background: rgba(255,255,255,0.95);
                margin: 20px;
                border-radius: 20px;
                padding: 25px;
                display: flex;
                flex-direction: column;
            }}
            
            .logo {{
                text-align: center;
                margin-bottom: 25px;
            }}
            
            .logo h1 {{
                color: #4a90e2;
                font-size: 1.8rem;
                margin-bottom: 5px;
            }}
            
            .logo p {{
                color: #666;
                font-size: 0.85rem;
            }}
            
            .current-state {{
                background: linear-gradient(135deg, #50c878 0%, #32cd32 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 20px;
                transition: all 0.5s ease;
            }}
            
            .current-state.changed {{
                background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
                transform: scale(1.02);
            }}
            
            .state-main {{
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            
            .state-name {{
                font-size: 1.1rem;
                margin-bottom: 5px;
            }}
            
            .state-family {{
                font-size: 0.85rem;
                opacity: 0.9;
            }}
            
            .session-info {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                font-size: 0.9rem;
            }}
            
            .session-info h4 {{
                color: #4a90e2;
                margin-bottom: 10px;
            }}
            
            .stat-item {{
                display: flex;
                justify-content: space-between;
                margin: 8px 0;
            }}
            
            .stat-value {{
                font-weight: bold;
                color: #28a745;
            }}
            
            .main-area {{
                flex: 1;
                display: flex;
                flex-direction: column;
                background: white;
                margin: 20px 20px 20px 0;
                border-radius: 20px;
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%);
                color: white;
                padding: 25px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 1.8rem;
                margin-bottom: 8px;
            }}
            
            .chat-container {{
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #fafafa;
            }}
            
            .message {{
                margin: 15px 0;
                animation: slideIn 0.3s ease;
            }}
            
            .user-message {{
                text-align: right;
            }}
            
            .user-bubble {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 18px;
                border-radius: 18px 18px 5px 18px;
                max-width: 70%;
                word-wrap: break-word;
            }}
            
            .ai-message {{
                display: flex;
                align-items: flex-start;
                gap: 12px;
            }}
            
            .ai-avatar {{
                width: 35px;
                height: 35px;
                border-radius: 50%;
                background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 1rem;
                flex-shrink: 0;
            }}
            
            .ai-content {{
                flex: 1;
                background: white;
                border-radius: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                overflow: hidden;
            }}
            
            .ai-response {{
                padding: 18px;
                line-height: 1.6;
            }}
            
            .ai-meta {{
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
                padding: 12px 18px;
                font-size: 0.85rem;
                color: #666;
            }}
            
            .state-transition {{
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 8px 18px;
                font-size: 0.8rem;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            
            .input-zone {{
                background: white;
                padding: 20px;
                border-top: 1px solid #e9ecef;
            }}
            
            .input-container {{
                display: flex;
                gap: 12px;
                align-items: flex-end;
            }}
            
            .input-field {{
                flex: 1;
                min-height: 45px;
                padding: 12px 18px;
                border: 2px solid #e9ecef;
                border-radius: 22px;
                font-size: 15px;
                resize: none;
                font-family: inherit;
                transition: border-color 0.3s ease;
            }}
            
            .input-field:focus {{
                outline: none;
                border-color: #4a90e2;
            }}
            
            .send-button {{
                width: 45px;
                height: 45px;
                border-radius: 50%;
                background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%);
                color: white;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
                transition: transform 0.2s ease;
            }}
            
            .send-button:hover {{
                transform: scale(1.05);
            }}
            
            .send-button:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .suggested-questions {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 12px;
            }}
            
            .suggested-question {{
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            
            .suggested-question:hover {{
                background: #e9ecef;
            }}
            
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
    </head>
    <body>
        <div class="app">
            <div class="sidebar">
                <div class="logo">
                    <h1>🌊 FlowMe</h1>
                    <p>Dialogue Conscient</p>
                </div>
                
                <div class="current-state" id="current-state-display">
                    <div class="state-main" id="current-state-id">1</div>
                    <div class="state-name" id="current-state-name">Présence</div>
                    <div class="state-family" id="current-state-family">Écoute Subtile</div>
                </div>
                
                <div class="session-info">
                    <h4>🗺️ Parcours</h4>
                    <div class="stat-item">
                        <span>Messages:</span>
                        <span class="stat-value" id="message-count">0</span>
                    </div>
                    <div class="stat-item">
                        <span>États explorés:</span>
                        <span class="stat-value" id="unique-states">1</span>
                    </div>
                    <div class="stat-item">
                        <span>Familles:</span>
                        <span class="stat-value" id="families-count">1</span>
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 10px; font-size: 0.8rem; color: #666; text-align: center; margin-top: auto;">
                    <strong>💡 FlowMe</strong><br>
                    Chaque message révèle un état de conscience. L'IA s'adapte à votre flux naturel.
                </div>
            </div>
            
            <div class="main-area">
                <div class="header">
                    <h1>Dialogue Conscient</h1>
                    <p>Explorez vos états de conscience en toute authenticité</p>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="message ai-message">
                        <div class="ai-avatar">F</div>
                        <div class="ai-content">
                            <div class="ai-response">
                                Bienvenue dans cet espace de dialogue conscient. 
                                <br><br>
                                <strong>Comment vous sentez-vous en ce moment ?</strong>
                                <br><br>
                                Exprimez-vous librement - tristesse, joie, questionnement, colère... 
                                Tout est accueilli avec bienveillance.
                            </div>
                            <div class="ai-meta">
                                💫 État actuel : Présence - Votre point de départ pour cette exploration
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="input-zone">
                    <div class="input-container">
                        <textarea 
                            class="input-field" 
                            placeholder="Exprimez-vous authentiquement..."
                            rows="1"
                            id="messageInput"
                        ></textarea>
                        <button class="send-button" onclick="sendMessage()">
                            ➤
                        </button>
                    </div>
                    
                    <div class="suggested-questions">
                        <div class="suggested-question" onclick="useQuestion('Je me sens un peu perdu')">
                            💭 Je me sens perdu
                        </div>
                        <div class="suggested-question" onclick="useQuestion('Comment puis-je changer ?')">
                            🔄 Comment changer ?
                        </div>
                        <div class="suggested-question" onclick="useQuestion('J\\'ai besoin de parler')">
                            💬 Besoin de parler
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const API_BASE = '{BACKEND_URL}';
            let messageCount = 0;
            let currentState = 1;
            let stateHistory = [1];
            let uniqueStates = new Set([1]);
            let familiesExplored = new Set(['Écoute Subtile']);
            
            // Auto-resize textarea
            document.getElementById('messageInput').addEventListener('input', function() {{
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            }});
            
            // Enter to send
            document.getElementById('messageInput').addEventListener('keypress', function(e) {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    sendMessage();
                }}
            }});
            
            function useQuestion(question) {{
                document.getElementById('messageInput').value = question;
                sendMessage();
            }}
            
            function sendMessage() {{
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                addUserMessage(message);
                input.value = '';
                input.style.height = 'auto';
                
                // Simuler analyse
                setTimeout(() => {{
                    analyzeAndRespond(message);
                }}, 800);
            }}
            
            function addUserMessage(message) {{
                const container = document.getElementById('chat-container');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message user-message';
                messageDiv.innerHTML = `<div class="user-bubble">${{message}}</div>`;
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }}
            
            async function analyzeAndRespond(message) {{
                try {{
                    const response = await fetch(`${{API_BASE}}/analyze/enhanced`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ 
                            message: message,
                            previous_states: stateHistory,
                            deep_analysis: true
                        }})
                    }});
                    
                    if (response.ok) {{
                        const data = await response.json();
                        const newState = data.detected_state;
                        const stateChanged = newState !== currentState;
                        
                        addAIMessage(data, stateChanged);
                        
                        if (stateChanged) {{
                            updateCurrentState(newState, data.state_info);
                            currentState = newState;
                        }}
                        
                        messageCount++;
                        stateHistory.push(newState);
                        uniqueStates.add(newState);
                        if (data.state_info?.famille_symbolique) {{
                            familiesExplored.add(data.state_info.famille_symbolique);
                        }}
                        updateStats();
                        
                    }} else {{
                        addSimpleAIMessage("Je vous écoute. Continuez à partager ce qui vous traverse.");
                    }}
                }} catch (error) {{
                    console.error('Erreur:', error);
                    addSimpleAIMessage("Je rencontre une difficulté technique, mais je reste à votre écoute.");
                }}
            }}
            
            function addAIMessage(data, stateChanged) {{
                const container = document.getElementById('chat-container');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ai-message';
                
                const advice = data.advice || "Je suis à votre écoute.";
                const stateName = data.state_info?.name || "Présence";
                const familyName = data.state_info?.famille_symbolique || "Écoute Subtile";
                
                messageDiv.innerHTML = `
                    <div class="ai-avatar">F</div>
                    <div class="ai-content">
                        <div class="ai-response">${{advice}}</div>
                        ${{stateChanged ? `<div class="state-transition">✨ Transition vers ${{stateName}}</div>` : ''}}
                        <div class="ai-meta">
                            État: ${{data.detected_state}} - ${{stateName}} (${{familyName}})
                        </div>
                    </div>
                `;
                
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }}
            
            function addSimpleAIMessage(text) {{
                const container = document.getElementById('chat-container');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ai-message';
                messageDiv.innerHTML = `
                    <div class="ai-avatar">F</div>
                    <div class="ai-content">
                        <div class="ai-response">${{text}}</div>
                    </div>
                `;
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }}
            
            function updateCurrentState(stateId, stateInfo) {{
                const display = document.getElementById('current-state-display');
                
                document.getElementById('current-state-id').textContent = stateId;
                document.getElementById('current-state-name').textContent = stateInfo?.name || 'Présence';
                document.getElementById('current-state-family').textContent = stateInfo?.famille_symbolique || 'Écoute Subtile';
                
                display.classList.add('changed');
                setTimeout(() => display.classList.remove('changed'), 2000);
            }}
            
            function updateStats() {{
                document.getElementById('message-count').textContent = messageCount;
                document.getElementById('unique-states').textContent = uniqueStates.size;
                document.getElementById('families-count').textContent = familiesExplored.size;
            }}
            
            // Focus initial
            document.getElementById('messageInput').focus();
        </script>
    </body>
    </html>
    """

@app.post("/analyze/enhanced")
async def analyze_message_enhanced(request: FlowAnalysisRequest):
    """Analyse complète avec interface épurée"""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message vide")
        
        context = {}
        if request.previous_states:
            context["etat_precedent"] = request.previous_states[-1]
        
        detected_state = detect_flowme_state(request.message, context)
        state_info = get_state_info(detected_state)
        advice = get_state_advice(detected_state, request.message, context)
        
        return {
            "status": "success",
            "detected_state": detected_state,
            "state_info": state_info,
            "advice": advice,
            "timestamp": datetime.now().isoformat(),
            "version": "3.1.0-clean"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check simplifié"""
    return {
        "status": "healthy",
        "version": "3.1.0-clean",
        "interface": "épurée",
        "detection_working": DETECTION_WORKING,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🌊 FlowMe v3.1.0 - Interface Épurée")
    print("✨ Démarrage avec interface focalisée utilisateur")
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
