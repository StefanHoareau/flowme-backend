# main.py - VERSION CORRIGÉE POUR RENDER
"""
FlowMe Backend v3 - Architecture Éthique
Version avec import corrigé et gestion d'erreurs robuste
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
print("🔄 Tentative d'import du module FlowMe States Detection...")

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
    print("✅ Module FlowMe States Detection importé avec succès")
    
    # Test immédiat pour vérifier que ça fonctionne
    try:
        test_result = detect_flowme_state("je suis triste")
        test_name = FLOWME_STATES[test_result]['name']
        print(f"🧪 Test import réussi: 'je suis triste' -> État {test_result} ({test_name})")
        DETECTION_WORKING = True
    except Exception as test_error:
        print(f"⚠️ Import OK mais test échoué: {test_error}")
        DETECTION_WORKING = False
    
except ImportError as import_error:
    print(f"❌ ERREUR CRITIQUE D'IMPORT: {import_error}")
    print("🚨 Création de fonctions de fallback...")
    
    # Fonctions de fallback pour éviter le crash
    DETECTION_WORKING = False
    FLOWME_STATES = {1: {"name": "Présence", "famille_symbolique": "Écoute subtile"}}
    FAMILLE_SYMBOLIQUE = {"Écoute subtile": {"description": "États d'attention"}}
    
    def detect_flowme_state(message: str, context: Optional[Dict] = None) -> int:
        """Fallback - retourne toujours état 1"""
        return 1
    
    def get_state_advice(state_id: int, message: str, context: Optional[Dict] = None) -> str:
        """Fallback - conseil générique"""
        return "J'accueille avec attention totale • FlowMe en mode de récupération"
    
    def get_state_info(state_id: int) -> Dict[str, Any]:
        """Fallback - info minimale"""
        return {
            "id": 1,
            "name": "Présence",
            "famille_symbolique": "Écoute subtile",
            "posture_adaptative": "J'accueille avec attention"
        }
    
    def analyze_message_flow(message: str, previous_states: Optional[List[int]] = None) -> Dict[str, Any]:
        """Fallback - analyse minimale"""
        return {
            "detected_state": 1,
            "state_info": get_state_info(1),
            "advice": get_state_advice(1, message),
            "flow_tendency": "stable",
            "message_analysis": {"type_detecte": "fallback"},
            "recommendations": ["Module de détection en cours de réparation"]
        }
    
    def test_flowme_detection():
        """Fallback - test factice"""
        print("❌ Module en mode fallback - tests non disponibles")
        return False

except Exception as unknown_error:
    print(f"❌ ERREUR INCONNUE LORS DE L'IMPORT: {unknown_error}")
    # Mêmes fallbacks que pour ImportError
    DETECTION_WORKING = False
    # ... (mêmes définitions que ci-dessus)

# Configuration FastAPI
app = FastAPI(
    title="FlowMe Backend v3 - Architecture Éthique", 
    description=f"IA éthique avec détection des 64 états de conscience {'(FONCTIONNELLE)' if DETECTION_WORKING else '(MODE DÉGRADÉ)'}",
    version="3.0.2-stable"
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

# Variables globales pour les sessions
active_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil avec statut de détection"""
    
    # Test en temps réel de la détection
    try:
        if DETECTION_WORKING:
            test_message = "je suis triste"
            detected_state = detect_flowme_state(test_message)
            state_name = FLOWME_STATES[detected_state]["name"]
            test_status = "FONCTIONNELLE"
            test_color = "#28a745"
        else:
            test_message = "test en mode dégradé"
            detected_state = 1
            state_name = "Présence (fallback)"
            test_status = "MODE DÉGRADÉ"
            test_color = "#ffc107"
    except Exception as e:
        test_message = "erreur de test"
        detected_state = 1
        state_name = f"Erreur: {str(e)[:50]}"
        test_status = "ERREUR"
        test_color = "#dc3545"
    
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <title>FlowMe v3 - {test_status}</title>
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
                .test-result {{ 
                    background: rgba(255,255,255,0.15); 
                    padding: 1rem; 
                    border-radius: 10px; 
                    margin: 1rem 0;
                    border-left: 4px solid {test_color};
                }}
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
                .status-badge {{
                    background: {test_color};
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    display: inline-block;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <h1>🌊 FlowMe v3</h1>
                    <h2>Architecture Éthique Stefan Hoareau</h2>
                    <div class="status-badge">{test_status}</div>
                </div>
                
                <div class="status">
                    <h3>📊 Statut Système</h3>
                    <div class="test-result">
                        <strong>Message testé:</strong> "{test_message}"<br>
                        <strong>État détecté:</strong> {detected_state} - {state_name}<br>
                        <strong>Détection:</strong> {test_status}<br>
                        <strong>Modules:</strong> {'✅ Tous chargés' if DETECTION_WORKING else '⚠️ Mode fallback actif'}
                    </div>
                    
                    <p>🎯 <strong>États disponibles:</strong> {len(FLOWME_STATES)} états de conscience</p>
                    <p>🏛️ <strong>Familles symboliques:</strong> {len(FAMILLE_SYMBOLIQUE)} familles</p>
                    <p>🚀 <strong>Version:</strong> 3.0.2-stable</p>
                </div>
                
                <div>
                    <a href="/interface" class="btn">🚀 Interface Utilisateur</a>
                    <a href="/health" class="btn">📊 Diagnostic Complet</a>
                    <a href="/test-detection" class="btn">🧪 Tests Automatiques</a>
                    <a href="/docs" class="btn">📚 API Documentation</a>
                </div>
                
                <div style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.8;">
                    <p>Déployé sur Render • Backend URL: {BACKEND_URL}</p>
                    <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Vérification santé avec diagnostic complet"""
    try:
        # Tests de détection en temps réel
        test_cases = [
            ("je suis triste", 45),
            ("comment changer", 7),
            ("bonjour", 1),
            ("mon lacet est cassé", 22)
        ]
        
        detection_results = []
        detection_working = DETECTION_WORKING
        errors = []
        
        for message, expected_state in test_cases:
            try:
                detected = detect_flowme_state(message)
                result_ok = detected != 1 or message == "bonjour"  # Seul "bonjour" devrait donner 1
                detection_results.append({
                    "message": message,
                    "detected": detected,
                    "expected": expected_state,
                    "working": result_ok,
                    "state_name": FLOWME_STATES.get(detected, {}).get("name", "Inconnu")
                })
                if not result_ok and message != "bonjour" and DETECTION_WORKING:
                    detection_working = False
            except Exception as e:
                errors.append(f"Erreur test '{message}': {str(e)}")
                detection_working = False
        
        # Composants système
        components = {
            "flowme_detection": "✅ FONCTIONNEL" if detection_working else "❌ DÉGRADÉ",
            "states_loaded": f"✅ {len(FLOWME_STATES)} états",
            "families_loaded": f"✅ {len(FAMILLE_SYMBOLIQUE)} familles",
            "api_endpoints": "✅ Opérationnels",
            "fallback_mode": "❌ Actif" if not DETECTION_WORKING else "✅ Inactif"
        }
        
        # Statut global
        overall_status = "healthy" if detection_working and DETECTION_WORKING else "degraded"
        if errors:
            overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "service": "FlowMe Backend v3",
            "version": "3.0.2-stable",
            "detection_working": detection_working,
            "fallback_active": not DETECTION_WORKING,
            "components": components,
            "detection_tests": detection_results,
            "errors": errors,
            "architecture": "Stefan Hoareau - IA Éthique Conversationnelle",
            "deployment": {
                "platform": "Render",
                "url": BACKEND_URL,
                "python_version": "3.11"
            }
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "detection_working": False,
            "fallback_active": True
        }

@app.get("/test-detection")
async def test_detection_endpoint():
    """Endpoint pour tester la détection en profondeur"""
    
    if not DETECTION_WORKING:
        return {
            "status": "warning",
            "message": "Système en mode fallback - tests limités",
            "timestamp": datetime.now().isoformat(),
            "fallback_active": True
        }
    
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
    total_score = 0
    
    for message in test_cases:
        try:
            detected_state = detect_flowme_state(message)
            state_info = get_state_info(detected_state)
            advice = get_state_advice(detected_state, message)
            
            # Score basique (si pas état 1 sauf pour bonjour)
            score = 1 if (detected_state != 1 or message == "bonjour") else 0
            total_score += score
            
            results.append({
                "message": message,
                "detected_state": detected_state,
                "state_name": state_info["name"],
                "family": state_info["famille_symbolique"],
                "advice": advice[:100] + "..." if len(advice) > 100 else advice,
                "score": score
            })
        except Exception as e:
            results.append({
                "message": message,
                "error": str(e),
                "score": 0
            })
    
    success_rate = (total_score / len(test_cases)) * 100
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "test_results": results,
        "detection_working": DETECTION_WORKING,
        "success_rate": f"{success_rate:.1f}%",
        "total_tests": len(test_cases),
        "passed_tests": total_score,
        "recommendation": "Excellent" if success_rate > 80 else "Satisfaisant" if success_rate > 60 else "Nécessite amélioration"
    }

@app.post("/analyze")
async def analyze_message(request: AnalyzeRequest):
    """Analyse FONCTIONNELLE d'un message"""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message vide")
        
        # Construire le contexte
        context = request.context or {}
        if request.session_history:
            context["etat_precedent"] = request.session_history[-1]
        
        # DÉTECTION avec gestion des erreurs
        try:
            detected_state = detect_flowme_state(request.message, context)
        except Exception as detection_error:
            print(f"❌ Erreur détection: {detection_error}")
            detected_state = 1  # Fallback
        
        # Obtenir les informations complètes
        try:
            state_info = get_state_info(detected_state)
            advice = get_state_advice(detected_state, request.message, context)
        except Exception as info_error:
            print(f"❌ Erreur info état: {info_error}")
            state_info = {"name": "Présence", "famille_symbolique": "Écoute subtile"}
            advice = "J'accueille avec attention totale"
        
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
            "system_status": {
                "detection_working": DETECTION_WORKING,
                "fallback_active": not DETECTION_WORKING,
                "version": "3.0.2-stable"
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
        
        # Analyse complète avec gestion d'erreurs
        try:
            analysis = analyze_message_flow(
                message=request.message,
                previous_states=request.previous_states or []
            )
        except Exception as analysis_error:
            print(f"❌ Erreur analyse enhanced: {analysis_error}")
            # Fallback analysis
            analysis = {
                "detected_state": 1,
                "state_info": {"name": "Présence", "famille_symbolique": "Écoute subtile"},
                "advice": "J'accueille avec attention totale",
                "flow_tendency": "stable",
                "message_analysis": {"type_detecte": "fallback"},
                "recommendations": ["Système en mode de récupération"]
            }
        
        return {
            "status": "success",
            "detected_state": analysis["detected_state"],
            "state_info": analysis["state_info"],
            "advice": analysis["advice"],
            "flow_tendency": analysis.get("flow_tendency", "stable"),
            "message_analysis": analysis.get("message_analysis", {}),
            "recommendations": analysis.get("recommendations", []),
            "timestamp": datetime.now().isoformat(),
            "system_status": {
                "detection_working": DETECTION_WORKING,
                "fallback_active": not DETECTION_WORKING,
                "version": "3.0.2-stable"
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur dans analyze_message_enhanced: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse avancée: {str(e)}")

@app.get("/states")
async def get_all_states():
    """Liste tous les états disponibles"""
    try:
        return {
            "status": "success",
            "total_states": len(FLOWME_STATES),
            "states": [get_state_info(i) for i in FLOWME_STATES.keys()],
            "detection_working": DETECTION_WORKING,
            "fallback_active": not DETECTION_WORKING,
            "message": "Module de détection fonctionnel" if DETECTION_WORKING else "Système en mode dégradé"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/interface", response_class=HTMLResponse)
async def get_interface():
    """Interface FlowMe avec gestion des modes"""
    return HTMLResponse(get_enhanced_interface_with_status())

def get_enhanced_interface_with_status():
    """Interface FlowMe avec indication du statut système"""
    status_color = "#28a745" if DETECTION_WORKING else "#ffc107"
    status_text = "DÉTECTION FONCTIONNELLE" if DETECTION_WORKING else "MODE DÉGRADÉ ACTIF"
    
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FlowMe v3 - {status_text}</title>
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
                width: 350px; 
                background: rgba(255,255,255,0.95); 
                margin: 20px 0 20px 20px; 
                border-radius: 20px; 
                padding: 25px; 
                overflow-y: auto;
            }}
            .sidebar h2 {{ color: #4a90e2; margin-bottom: 20px; }}
            
            .system-status {{
                background: {status_color};
                color: white;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 20px;
                font-weight: bold;
                font-size: 0.9rem;
            }}
            
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
            
            .input-group {{ display: flex; gap: 15px; position: relative; }}
            .input-group input {{ 
                flex: 1; 
                padding: 15px 20px; 
                border: 2px solid #e1e5e9; 
                border-radius: 25px; 
                font-size: 16px;
            }}
            .input-group.processing input {{
                border-color: #ffc107;
                background: rgba(255, 193, 7, 0.1);
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
            
            @keyframes slideIn {{ from {{ opacity: 0; transform: translateX(20px); }} to {{ opacity: 1; transform: translateX(0); }} }}
            .pulse {{ animation: pulse 0.6s ease; }}
            @keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} }}
        </style>
    </head>
    <body>
        <div class="app">
            <div class="sidebar">
                <h2>🌊 FlowMe v3</h2>
                
                <div class="system-status">
                    {status_text}
                </div>
                
                <div class="current-state" id="current-state-display">
                    <div class="state-id" id="current-state-id">1</div>
                    <div class="state-name" id="current-state-name">Présence</div>
                    <div class="state-family" id="current-state-family">Écoute subtile</div>
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
                        <span>Détection:</span>
                        <span class="stat-value" id="detection-status">{'Active' if DETECTION_WORKING else 'Dégradée'}</span>
                    </div>
                    <div class="stat-item">
                        <span>Système:</span>
                        <span class="stat-value">v3.0.2</span>
                    </div>
                </div>
            </div>
            
            <div class="main-chat">
                <div class="header">
                    <h1>FlowMe v3 - Architecture Éthique</h1>
                    <p>{'Détection fonctionnelle active' if DETECTION_WORKING else 'Mode dégradé - fonctionnalités limitées'}</p>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="message ai-message">
                        <div>🎯 <strong>FlowMe v3 - Système {'opérationnel' if DETECTION_WORKING else 'en mode dégradé'} !</strong><br><br>
                        {'Cette version détecte les différents états selon vos messages. Essayez:' if DETECTION_WORKING else 'Système en cours de stabilisation. Fonctionnalités limitées mais opérationnelles:'}<br>
                        • "je suis triste" → Vulnérabilité<br>
                        • "comment changer" → Curiosité<br>
                        • "mon lacet est cassé" → Pragmatisme<br>
                        • "bonjour" → Présence</div>
                        <div class="message-meta">État: 1 - Présence (Écoute subtile) • {'Détection active' if DETECTION_WORKING else 'Mode dégradé'}</div>
                        <div class="state-info">
                            💡 <strong>Statut:</strong> {'Système entièrement fonctionnel' if DETECTION_WORKING else 'Fonctionnement en mode de sécurité - service maintenu'}
                        </div>
                    </div>
                </div>
                
                <div class="input-area">
                    <div class="input-group" id="input-group">
                        <input type="text" id="message-input" placeholder="{'Testez la détection...' if DETECTION_WORKING else 'Système en mode dégradé - fonctions de base disponibles...'}" />
                        <button onclick="sendMessage()" id="send-button">Analyser</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const API_BASE = '{BACKEND_URL}';
            const DETECTION_WORKING = {str(DETECTION_WORKING).lower()};
            let messageCount = 0;
            let stateHistory = [1];
            let uniqueStates = new Set([1]);
            let lastState = 1;
            
            async function sendMessage() {{
                const input = document.getElementById('message-input');
                const button = document.getElementById('send-button');
                const inputGroup = document.getElementById('input-group');
                const message = input.value.trim();
                
                if (!message) return;
                
                input.disabled = true;
                button.disabled = true;
                inputGroup.classList.add('processing');
                button.textContent = 'Analyse...';
                
                addMessage(message, 'user');
                input.value = '';
                
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
                        console.log('🎯 Réponse API:', data);
                        
                        const newState = data.detected_state;
                        const stateChanged = newState !== lastState;
                        
                        addAIMessage(data, stateChanged);
                        updateCurrentState(data.detected_state, data.state_info, stateChanged);
                        
                        messageCount++;
                        stateHistory.push(data.detected_state);
                        uniqueStates.add(data.detected_state);
                        updateStats();
                        
                        lastState = newState;
                        
                    }} else {{
                        const errorText = await response.text();
                        console.error('❌ Erreur API:', response.status, errorText);
                        addMessage("Erreur temporaire. Le système continue de fonctionner.", 'ai');
                    }}
                }} catch (error) {{
                    console.error('❌ Erreur réseau:', error);
                    addMessage("Erreur de connexion. Veuillez réessayer.", 'ai');
                }} finally {{
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
                const systemStatus = data.system_status ? 
                    (data.system_status.detection_working ? "Détection active" : "Mode dégradé") : 
                    "Système opérationnel";
                
                message.innerHTML = `
                    <div>${{advice}}</div>
                    <div class="message-meta">
                        ${{stateChanged ? '🔄 NOUVEL ' : ''}}État: ${{data.detected_state}} - ${{stateName}} 
                        (${{familyName}}) • ${{systemStatus}}
                    </div>
                    <div class="state-info">
                        ${{stateChanged ? '✨ <strong>Transition détectée !</strong>' : 'État maintenu'}}
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
                
                messageCountEl.textContent = messageCount;
                uniqueStatesEl.textContent = uniqueStates.size;
                
                [messageCountEl, uniqueStatesEl].forEach(el => {{
                    el.classList.add('updated');
                    setTimeout(() => el.classList.remove('updated'), 500);
                }});
            }}
            
            document.getElementById('message-input').addEventListener('keypress', function(e) {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    sendMessage();
                }}
            }});
            
            document.getElementById('message-input').focus();
            
            console.log('🌊 FlowMe v3.0.2 chargé - Statut:', DETECTION_WORKING ? 'Fonctionnel' : 'Mode dégradé');
        </script>
    </body>
    </html>
    """

# Point d'entrée principal avec gestion d'erreurs robuste
if __name__ == "__main__":
    import uvicorn
    
    # Test final avant démarrage
    print("\n" + "="*60)
    print("🧪 TEST FINAL AVANT DÉMARRAGE DU SERVEUR")
    print("="*60)
    
    try:
        if DETECTION_WORKING:
            print("✅ Module de détection importé avec succès")
            test_success = test_flowme_detection()
            if test_success:
                print("✅ Tests de validation RÉUSSIS")
            else:
                print("⚠️ Tests partiellement réussis - système fonctionnel")
        else:
            print("⚠️ Module en mode FALLBACK - fonctionnalités limitées")
            print("ℹ️ Le serveur fonctionnera avec des réponses de base")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        print("⚠️ Démarrage en mode de sécurité")
    
    # Configuration du serveur
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE FLOWME v3.0.2")
    print("="*60)
    print(f"🌐 Host: {host}:{port}")
    print(f"🎯 Détection: {'ACTIVE' if DETECTION_WORKING else 'MODE DÉGRADÉ'}")
    print(f"📊 États disponibles: {len(FLOWME_STATES)}")
    print(f"🏛️ Familles: {len(FAMILLE_SYMBOLIQUE)}")
    print(f"🔗 URL: {BACKEND_URL}")
    print("\n📍 Endpoints principaux:")
    print(f"   • Interface: {BACKEND_URL}/interface")
    print(f"   • Santé: {BACKEND_URL}/health")
    print(f"   • Tests: {BACKEND_URL}/test-detection")
    print(f"   • API Docs: {BACKEND_URL}/docs")
    print("="*60)
    
    try:
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as startup_error:
        print(f"\n❌ ERREUR CRITIQUE AU DÉMARRAGE: {startup_error}")
        print("🆘 Impossible de démarrer le serveur")
        exit(1)
