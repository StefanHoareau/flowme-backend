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
                        <h3>💎
