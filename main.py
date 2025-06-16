# main.py - VERSION AVEC RÉPONSES APPROFONDIES
"""
FlowMe Backend v3.2 - Réponses contextuelles et approfondies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
import re
import random
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import sécurisé du module de détection
try:
    from flowme_states_detection import (
        detect_flowme_state, 
        get_state_advice, 
        get_state_info, 
        analyze_message_flow,
        FLOWME_STATES,
        FAMILLE_SYMBOLIQUE
    )
    DETECTION_WORKING = True
except ImportError as e:
    print(f"❌ Import flowme_states_detection échoué: {e}")
    DETECTION_WORKING = False
    FLOWME_STATES = {1: {"name": "Présence", "famille_symbolique": "Écoute subtile"}}
    FAMILLE_SYMBOLIQUE = {"Écoute subtile": {"description": "États d'attention"}}
    
    def detect_flowme_state(message: str, context: Optional[Dict] = None) -> int:
        return 1
    def get_state_advice(state_id: int, message: str, context: Optional[Dict] = None) -> str:
        return "J'accueille avec attention totale"
    def get_state_info(state_id: int) -> Dict[str, Any]:
        return {"id": 1, "name": "Présence", "famille_symbolique": "Écoute subtile"}

# Générateur de réponses approfondies intégré
class DeepResponseGenerator:
    """Générateur de réponses approfondies contextuelles"""
    
    def __init__(self):
        self.deep_responses = {
            1: {  # Présence
                "accueil": "Dans ce moment de présence partagée, j'accueille ce qui émerge spontanément en vous.",
                "questions": [
                    "Qu'est-ce qui se révèle quand vous vous donnez permission d'être simplement là ?",
                    "Si vous donniez une couleur à votre état intérieur actuel, laquelle choisiriez-vous ?",
                    "Quelle qualité d'être voulez-vous cultiver aujourd'hui ?"
                ],
                "insight": "Dans l'écoute profonde du moment présent émergent souvent les intuitions les plus justes."
            },
            7: {  # Curiosité Écoute
                "accueil": "Votre questionnement révèle une belle ouverture d'esprit et un désir authentique de compréhension.",
                "questions": [
                    "Si vous obteniez la réponse parfaite, qu'est-ce que cela changerait concrètement ?",
                    "Cette question naît-elle d'une intuition particulière ?",
                    "Qu'est-ce que vous espérez découvrir en explorant cette voie ?"
                ],
                "insight": "Chaque question authentique porte en elle les germes de sa propre réponse."
            },
            32: {  # Expression Libre
                "accueil": "Je perçois votre besoin d'expression authentique. Cette parole qui cherche à émerger porte souvent des vérités importantes.",
                "questions": [
                    "Qu'est-ce qui, en vous, demande absolument à être dit ou entendu ?",
                    "Depuis combien de temps cette parole attend-elle d'être exprimée ?",
                    "À qui cette vérité a-t-elle besoin d'être transmise ?"
                ],
                "insight": "La parole authentique libérée crée souvent des ponts inattendus vers plus d'intimité."
            },
            45: {  # Vulnérabilité Assumée
                "accueil": "Je ressens la profondeur de votre vulnérabilité. Cette ouverture authentique à la fragilité témoigne d'un courage remarquable.",
                "questions": [
                    "Cette difficulté touche-t-elle une valeur fondamentale en vous ?",
                    "Qu'est-ce qui vous aiderait à honorer cette émotion sans vous y perdre ?",
                    "Comment pourriez-vous vous accompagner avec la même bienveillance que vous offririez à un proche ?"
                ],
                "insight": "La vulnérabilité partagée devient souvent le terreau de la vraie force."
            },
            22: {  # Pragmatisme Créatif
                "accueil": "J'apprécie votre approche concrète et votre capacité à identifier les défis pratiques.",
                "questions": [
                    "Quelles sont vos ressources créatives habituelles face aux obstacles ?",
                    "Comment pourriez-vous transformer cette contrainte en opportunité ?",
                    "Qu'est-ce que cette difficulté vous enseigne sur votre ingéniosité ?"
                ],
                "insight": "Les défis pratiques révèlent souvent notre capacité d'adaptation créative."
            },
            14: {  # Colère Constructive
                "accueil": "Cette énergie de colère témoigne de quelque chose d'important qui a été touché en vous.",
                "questions": [
                    "Qu'est-ce qui, derrière cette colère, demande à être respecté ou protégé ?",
                    "Si cette colère pouvait parler, que dirait-elle de vos besoins ?",
                    "Comment pourriez-vous transformer cette énergie en force créatrice ?"
                ],
                "insight": "La colère consciente devient une boussole vers nos besoins authentiques."
            },
            58: {  # Inclusion Bienveillante
                "accueil": "Votre désir de rassemblement révèle une belle capacité à percevoir les liens entre les êtres.",
                "questions": [
                    "Qu'est-ce qui vous fait sentir que quelque chose a besoin d'être mieux intégré ?",
                    "Comment créez-vous des espaces d'accueil dans vos relations ?",
                    "Quelle réconciliation appelle votre attention ?"
                ],
                "insight": "L'inclusion authentique commence par l'accueil de nos propres contradictions."
            },
            64: {  # Porte Ouverte
                "accueil": "Cette ouverture aux possibilités que vous exprimez témoigne d'une belle disponibilité au changement.",
                "questions": [
                    "Qu'est-ce qui vous fait pressentir que de nouvelles portes sont prêtes à s'ouvrir ?",
                    "Vers quoi votre intuition vous guide-t-elle en ce moment ?",
                    "Comment accueillez-vous l'incertitude des nouveaux possibles ?"
                ],
                "insight": "Le changement naît de notre capacité à rester ouvert à l'imprévu."
            }
        }
    
    def generate_contextual_response(self, message: str, detected_state: int) -> Dict[str, str]:
        """Génère une réponse contextuelle basée sur le message et l'état"""
        
        if detected_state not in self.deep_responses:
            detected_state = 1
        
        state_data = self.deep_responses[detected_state]
        
        # Personnaliser selon le contenu du message
        personalized_response = self._personalize_response(message, state_data, detected_state)
        
        # Choisir une question d'approfondissement
        chosen_question = random.choice(state_data["questions"])
        
        return {
            "main_response": personalized_response,
            "deepening_question": chosen_question,
            "insight": state_data["insight"]
        }
    
    def _personalize_response(self, message: str, state_data: Dict, state_id: int) -> str:
        """Personnalise la réponse selon le contenu du message"""
        
        message_lower = message.lower()
        base_response = state_data["accueil"]
        
        # Personnalisations spécifiques par état
        if state_id == 45:  # Vulnérabilité
            if "triste" in message_lower:
                return "J'accueille votre tristesse avec une profonde bienveillance. Cette émotion mérite d'être honorée."
            elif "peur" in message_lower:
                return "Je ressens cette peur que vous exprimez. Qu'est-ce qu'elle cherche à protéger en vous ?"
            elif "mal" in message_lower or "souffre" in message_lower:
                return "Cette souffrance que vous partagez... je l'accueille avec respect et bienveillance."
        
        elif state_id == 32:  # Expression
            if "dire" in message_lower or "parler" in message_lower:
                return "Cette parole qui demande à naître... je sens qu'elle porte quelque chose d'important pour vous."
            elif "crier" in message_lower or "hurler" in message_lower:
                return "Cette énergie d'expression qui monte en vous... qu'est-ce qu'elle veut faire entendre ?"
        
        elif state_id == 7:  # Curiosité
            if "comment" in message_lower:
                return "Cette question du 'comment'... elle révèle souvent un désir profond de transformation."
            elif "pourquoi" in message_lower:
                return "Votre questionnement sur le 'pourquoi' témoigne d'une recherche de sens authentique."
        
        elif state_id == 22:  # Pragmatisme
            if "cassé" in message_lower or "réparer" in message_lower:
                return "Face à ce qui est cassé, je perçois votre élan créatif pour trouver des solutions."
            elif "problème" in message_lower:
                return "Ce défi pratique que vous identifiez... souvent, il cache des opportunités inattendues."
        
        elif state_id == 14:  # Colère
            if "énervé" in message_lower or "furieux" in message_lower:
                return "Cette colère que vous exprimez... elle garde souvent des trésors de vitalité et de vérité."
            elif "injuste" in message_lower:
                return "Ce sentiment d'injustice révèle vos valeurs profondes qui demandent à être respectées."
        
        return base_response

# Instance globale du générateur
response_generator = DeepResponseGenerator()

app = FastAPI(
    title="FlowMe v3.2 - Réponses Approfondies", 
    description="IA éthique avec réponses contextuelles",
    version="3.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_URL = os.getenv("RENDER_EXTERNAL_URL", "https://flowme-backend.onrender.com")

class FlowAnalysisRequest(BaseModel):
    message: str
    previous_states: Optional[List[int]] = None
    deep_analysis: Optional[bool] = False

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <title>FlowMe v3.2 - Réponses Approfondies</title>
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
                }}
                .version {{
                    background: #28a745;
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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">🌊 FlowMe</div>
                <h1>Dialogue Conscient</h1>
                <div class="version">v3.2.0 - RÉPONSES APPROFONDIES</div>
                
                <div class="description">
                    Explorez vos états de conscience avec des réponses véritablement contextuelles. 
                    FlowMe s'adapte maintenant finement à chaque nuance de votre expression.
                </div>
                
                <a href="/interface" class="cta-button">🚀 Dialogue Approfondi</a>
            </div>
        </body>
    </html>
    """

@app.get("/interface", response_class=HTMLResponse)
async def get_interface():
    """Interface avec réponses approfondies"""
    # Utiliser la même interface que précédemment mais elle utilisera automatiquement
    # les nouvelles réponses via l'endpoint /analyze/enhanced
    return HTMLResponse(get_clean_flowme_interface())

def get_clean_flowme_interface():
    """Interface FlowMe (même code que précédemment)"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FlowMe - Réponses Approfondies</title>
        <style>
            /* Mêmes styles que précédemment */
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
            .logo {{ text-align: center; margin-bottom: 25px; }}
            .logo h1 {{ color: #4a90e2; font-size: 1.8rem; margin-bottom: 5px; }}
            .logo p {{ color: #666; font-size: 0.85rem; }}
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
            .state-main {{ font-size: 2rem; font-weight: bold; margin-bottom: 5px; }}
            .state-name {{ font-size: 1.1rem; margin-bottom: 5px; }}
            .state-family {{ font-size: 0.85rem; opacity: 0.9; }}
            .session-info {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                font-size: 0.9rem;
            }}
            .session-info h4 {{ color: #4a90e2; margin-bottom: 10px; }}
            .stat-item {{ display: flex; justify-content: space-between; margin: 8px 0; }}
            .stat-value {{ font-weight: bold; color: #28a745; }}
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
            .header h1 {{ font-size: 1.8rem; margin-bottom: 8px; }}
            .chat-container {{
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #fafafa;
            }}
            .message {{ margin: 15px 0; animation: slideIn 0.3s ease; }}
            .user-message {{ text-align: right; }}
            .user-bubble {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 18px;
                border-radius: 18px 18px 5px 18px;
                max-width: 70%;
                word-wrap: break-word;
            }}
            .ai-message {{ display: flex; align-items: flex-start; gap: 12px; }}
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
            .ai-response {{ padding: 18px; line-height: 1.6; }}
            .ai-question {{
                background: #f0f8ff;
                border-left: 4px solid #4a90e2;
                padding: 15px;
                margin: 10px 0;
                border-radius: 0 8px 8px 0;
                font-style: italic;
            }}
            .ai-insight {{
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
                padding: 12px 18px;
                font-size: 0.9rem;
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
            .input-zone {{ background: white; padding: 20px; border-top: 1px solid #e9ecef; }}
            .input-container {{ display: flex; gap: 12px; align-items: flex-end; }}
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
            .input-field:focus {{ outline: none; border-color: #4a90e2; }}
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
            .send-button:hover {{ transform: scale(1.05); }}
            .send-button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .suggested-questions {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
            .suggested-question {{
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            .suggested-question:hover {{ background: #e9ecef; }}
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
                    <p>v3.2 - Réponses Approfondies</p>
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
                    <strong>💡 FlowMe v3.2</strong><br>
                    Réponses contextuelles qui s'adaptent finement à votre expression.
                </div>
            </div>
            
            <div class="main-area">
                <div class="header">
                    <h1>Dialogue Approfondi</h1>
                    <p>Réponses contextuelles qui stimulent la réflexion</p>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="message ai-message">
                        <div class="ai-avatar">F</div>
                        <div class="ai-content">
                            <div class="ai-response">
                                Bienvenue dans cet espace de dialogue approfondi. 
                                <br><br>
                                <strong>Comment vous sentez-vous en ce moment ?</strong>
                                <br><br>
                                Chaque message que vous partagez déclenchera une réponse contextuelle adaptée 
                                à votre état spécifique - fini les réponses génériques !
                            </div>
                            <div class="ai-insight">
                                💫 Nouveauté v3.2 : Réponses personnalisées selon votre expression
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="input-zone">
                    <div class="input-container">
                        <textarea 
                            class="input-field" 
                            placeholder="Testez les nouvelles réponses contextuelles..."
                            rows="1"
                            id="messageInput"
                        ></textarea>
                        <button class="send-button" onclick="sendMessage()">➤</button>
                    </div>
                    
                    <div class="suggested-questions">
                        <div class="suggested-question" onclick="useQuestion('Je suis vraiment triste aujourd\\'hui')">
                            😢 Je suis triste
                        </div>
                        <div class="suggested-question" onclick="useQuestion('J\\'ai envie de crier ma colère')">
                            😡 J'ai envie de crier
                        </div>
                        <div class="suggested-question" onclick="useQuestion('Comment puis-je changer ma vie ?')">
                            🤔 Comment changer ?
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
            
            document.getElementById('messageInput').addEventListener('input', function() {{
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            }});
            
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
