from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import re
import requests
from datetime import datetime
from typing import Dict, List, Optional
import os

app = FastAPI(title="FlowmeLocal v3 - Architecture 64 États", version="3.0.0")

# 🔧 CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🗄️ Configuration NocoDB
NOCODB_URL = "https://app.nocodb.com"
NOCODB_API_KEY = "*clIA2FsFLtJGK*t1p0PTbrMD-GXVw9WrLIdjVwe"
NOCODB_TABLE_ID = "m8lwhj640ohzg7m"

# 📊 Les 64 États de l'Architecture Éthique
ETATS_64 = {
    1: {
        "nom": "Présence Silencieuse",
        "famille": "Écoute subtile",
        "tension": "Latente, intérieure",
        "mot_cle": "Perception",
        "declencheurs": ["silence lourd", "malaise subtil", "tension non dite"],
        "posture": "Suspendre tout traitement analytique immédiat; Observer les signaux faibles",
        "compatibles": [8, 32, 45, 59, 64],
        "sequentiels": [2, 8, 10, 11],
        "conseil": "Quand tout semble brumeux, c'est dans le silence que la clarté peut émerger"
    },
    2: {
        "nom": "Montée de Pression",
        "famille": "Mutation latente", 
        "tension": "Intérieure, croissante",
        "mot_cle": "Anticipation",
        "declencheurs": ["tension qui monte", "énergie comprimée", "situation mal digérée"],
        "posture": "Sens le gonflement des tensions silencieuses",
        "compatibles": [1, 7, 12, 28],
        "sequentiels": [3, 7, 9, 12],
        "conseil": "Le vent s'accumule avant la tempête. Relâche maintenant pour éviter l'explosion"
    },
    # ... (continuer avec tous les 64 états)
    17: {
        "nom": "Frénésie",
        "famille": "Montée & excès",
        "tension": "Chaotique, expansive", 
        "mot_cle": "Dissolution",
        "declencheurs": ["emballement", "trop d'urgences", "élan déstructuré"],
        "posture": "Ralentir. Observer les points de tension",
        "compatibles": [3, 9, 25],
        "sequentiels": [18, 20, 24],
        "conseil": "Quand mille oiseaux s'envolent, le ciel ne s'éclaire pas. Il s'aveugle"
    },
    37: {
        "nom": "Volonté excessive",
        "famille": "Montée & excès",
        "tension": "Impulsionnelle, dirigée",
        "mot_cle": "Précipitation", 
        "declencheurs": ["impatience", "force excessive", "résultat forcé"],
        "posture": "Modérer l'intention par observation du courant",
        "compatibles": [14, 19, 38],
        "sequentiels": [38, 39, 40],
        "conseil": "Le torrent croit aller plus vite que la montagne. Mais c'est la roche qui lui dessine son chant"
    },
    44: {
        "nom": "Geste résonant",
        "famille": "Réveil & accord",
        "tension": "Fluide, incarnée",
        "mot_cle": "Impact doux",
        "declencheurs": ["action alignée", "geste juste", "simplicité efficace"],
        "posture": "Soutenir le déploiement sans surcharge",
        "compatibles": [36, 43, 56, 61],
        "sequentiels": [43, 45, 61],
        "conseil": "La goutte ne cherche pas à creuser la pierre. Mais c'est elle qui la transforme"
    },
    64: {
        "nom": "Porte ouverte",
        "famille": "Écoute subtile", 
        "tension": "Libre, inachevée",
        "mot_cle": "Disponibilité totale",
        "declencheurs": ["réceptivité radicale", "absence d'intention", "espace d'accueil"],
        "posture": "Soutenir la disponibilité intégrale sans refermer",
        "compatibles": [1, 32, 45, 59],
        "sequentiels": [1, 45, 59],
        "conseil": "Il n'y a plus de clé, plus de seuil. Il n'y a qu'un passage, et ta présence qui le rend possible"
    }
}

def detect_etat_flowme(text: str, contexte: Dict = None) -> Dict:
    """
    Détection d'état selon l'architecture des 64 états de Stefan Hoareau
    """
    text_norm = text.lower().strip()
    
    # Mots-clés pour détecter les états principaux
    patterns_etats = {
        1: ["silence", "malaise", "tension", "brumeux", "flou"],
        2: ["pression", "monte", "s'accumule", "tendu", "comprimé"],
        17: ["frénésie", "emballement", "trop", "urgent", "chaos"],
        37: ["force", "impatient", "pousse", "précipité", "volonté"],
        44: ["juste", "simple", "efficace", "doux", "résonant"],
        64: ["ouvert", "disponible", "accueil", "espace", "libre"]
    }
    
    etat_detecte = 1  # Par défaut: Présence Silencieuse
    confiance = 0.1
    
    # Analyser le texte pour trouver l'état correspondant
    for etat_id, mots_cles in patterns_etats.items():
        score = sum(1 for mot in mots_cles if mot in text_norm)
        if score > 0:
            nouvelle_confiance = min(0.9, 0.6 + (score * 0.1))
            if nouvelle_confiance > confiance:
                etat_detecte = etat_id
                confiance = nouvelle_confiance
    
    etat_info = ETATS_64.get(etat_detecte, ETATS_64[1])
    
    return {
        "etat_id": etat_detecte,
        "etat_nom": etat_info["nom"],
        "famille": etat_info["famille"],
        "tension": etat_info["tension"],
        "mot_cle": etat_info["mot_cle"],
        "confiance": round(confiance, 2),
        "conseil_flowme": etat_info["conseil"],
        "posture_adaptative": etat_info["posture"],
        "etats_compatibles": etat_info["compatibles"],
        "etats_sequentiels": etat_info["sequentiels"],
        "analyse": {
            "text_analysé": text,
            "longueur": len(text),
            "timestamp": datetime.now().isoformat(),
            "methode": "flowme_64_etats_v3"
        }
    }

async def save_to_nocodb(data: Dict) -> Dict:
    """Sauvegarder l'analyse dans NocoDB"""
    try:
        headers = {
            "Content-Type": "application/json",
            "xc-token": NOCODB_API_KEY
        }
        
        # Adapter les données pour NocoDB selon la structure visible
        nocodb_data = {
            "etat_id_flowme": data["etat_id"],
            "etat_nom": data["etat_nom"], 
            "tension_dominante": data["tension"],
            "famille_symbolique": data["famille"],
            "posture_adaptative": data["posture_adaptative"],
            "timestamp": datetime.now().isoformat(),
            "session_id": data.get("session_id", "default"),
            "score_bien_etre": data["confiance"],
            "recommendations": data["conseil_flowme"],
            "evolution_tendance": f"État {data['etat_id']} détecté"
        }
        
        url = f"{NOCODB_URL}/api/v1/db/data/noco/{NOCODB_TABLE_ID}/Reactions_Mistral"
        
        response = requests.post(url, json=nocodb_data, headers=headers)
        
        if response.status_code in [200, 201]:
            return {"success": True, "nocodb_id": response.json().get("Id")}
        else:
            return {"success": False, "error": f"Status {response.status_code}: {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
def read_root():
    return {
        "message": "FlowmeLocal v3 - Architecture 64 États opérationnelle",
        "version": "3.0.0",
        "author": "Stefan Hoareau",
        "architecture": "64 États de conscience adaptative",
        "endpoints": ["/analyze", "/etat/{id}", "/transition", "/nocodb/save"]
    }

@app.post("/analyze")
async def analyze_flowme(request: Request):
    """Analyse FlowmeLocal avec les 64 états"""
    try:
        data = await request.json()
        text = data.get("text", "")
        contexte = data.get("contexte", {})
        session_id = data.get("session_id", f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Le texte est requis")
        
        # Détecter l'état FlowMe
        resultat = detect_etat_flowme(text, contexte)
        resultat["session_id"] = session_id
        
        # Sauvegarder dans NocoDB
        sauvegarde = await save_to_nocodb(resultat)
        resultat["nocodb_save"] = sauvegarde
        
        return {
            "success": True,
            "flowme_analysis": resultat,
            "meta": {
                "api_version": "3.0.0",
                "architecture": "64_etats_ethiques",
                "saved_to_nocodb": sauvegarde["success"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@app.get("/etat/{etat_id}")
def get_etat_info(etat_id: int):
    """Récupérer les informations d'un état spécifique"""
    if etat_id not in ETATS_64:
        raise HTTPException(status_code=404, detail=f"État {etat_id} non trouvé")
    
    return {
        "etat_id": etat_id,
        "info": ETATS_64[etat_id],
        "architecture": "64_etats_flowme"
    }

@app.post("/transition")
async def suggest_transition(request: Request):
    """Suggérer une transition d'état"""
    try:
        data = await request.json()
        etat_actuel = data.get("etat_actuel", 1)
        intention = data.get("intention", "equilibre")
        
        if etat_actuel not in ETATS_64:
            raise HTTPException(status_code=400, detail="État actuel invalide")
        
        etat_info = ETATS_64[etat_actuel]
        
        # Suggérer des états compatibles ou séquentiels
        suggestions = []
        
        if intention == "apaisement":
            # Privilégier les états de la famille "Recul & germination"
            suggestions = [10, 15, 26, 35, 52]
        elif intention == "action":
            # Privilégier les états "Réveil & accord" 
            suggestions = [11, 12, 23, 44, 56]
        elif intention == "equilibre":
            # Utiliser les états compatibles
            suggestions = etat_info["compatibles"]
        else:
            # États séquentiels par défaut
            suggestions = etat_info["sequentiels"]
        
        transitions = []
        for etat_id in suggestions[:3]:  # Top 3
            if etat_id in ETATS_64:
                transitions.append({
                    "etat_id": etat_id,
                    "nom": ETATS_64[etat_id]["nom"],
                    "famille": ETATS_64[etat_id]["famille"],
                    "conseil": ETATS_64[etat_id]["conseil"]
                })
        
        return {
            "etat_actuel": {
                "id": etat_actuel,
                "nom": etat_info["nom"],
                "famille": etat_info["famille"]
            },
            "transitions_suggerees": transitions,
            "intention": intention
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transition: {str(e)}")

@app.get("/nocodb/history")
async def get_nocodb_history(limit: int = 10):
    """Récupérer l'historique des analyses depuis NocoDB"""
    try:
        headers = {"xc-token": NOCODB_API_KEY}
        url = f"{NOCODB_URL}/api/v1/db/data/noco/{NOCODB_TABLE_ID}/Reactions_Mistral"
        
        params = {"limit": limit, "sort": "-timestamp"}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
                "count": len(response.json().get("list", []))
            }
        else:
            return {"success": False, "error": f"Status {response.status_code}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
