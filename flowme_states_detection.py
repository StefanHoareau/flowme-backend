"""
FlowMe States Detection - Module de détection des 64 états de conscience
Basé sur l'architecture éthique de Stefan Torregrossa
"""

import re
import random
from typing import Dict, List, Any
from datetime import datetime

# Définition des 64 états FlowMe (inspirés du I-Ching adapté pour l'IA)
FLOWME_STATES = {
    1: {
        "name": "Présence Silencieuse",
        "description": "État d'écoute profonde et d'attention pure",
        "keywords": ["silence", "écoute", "attention", "présence", "calme"],
        "energy": "receptive",
        "advice_template": "Je ressens votre besoin d'être entendu. Prenons le temps de bien cerner votre situation."
    },
    2: {
        "name": "Terre Nourricière",
        "description": "Accueil bienveillant et soutien inconditionnel",
        "keywords": ["soutien", "aide", "accompagnement", "difficile", "problème"],
        "energy": "nurturing",
        "advice_template": "Je suis là pour vous accompagner. Ensemble, nous trouverons des solutions adaptées."
    },
    3: {
        "name": "Germination",
        "description": "Début d'un processus, émergence d'une idée",
        "keywords": ["nouveau", "commencer", "idée", "projet", "début"],
        "energy": "creative",
        "advice_template": "C'est le moment propice pour planter les graines de votre projet. Avançons pas à pas."
    },
    4: {
        "name": "Sagesse Enfantine",
        "description": "Curiosité pure et questionnement innocent",
        "keywords": ["pourquoi", "comment", "apprendre", "comprendre", "expliquer"],
        "energy": "curious",
        "advice_template": "Votre curiosité est précieuse. Explorons ensemble pour mieux comprendre."
    },
    5: {
        "name": "Patience Active",
        "description": "Attente consciente du bon moment",
        "keywords": ["attendre", "patience", "moment", "quand", "timing"],
        "energy": "patient",
        "advice_template": "Parfois, la meilleure action est de laisser mûrir la situation. Restons attentifs aux signes."
    },
    6: {
        "name": "Conflit Constructif",
        "description": "Gestion harmonieuse des tensions",
        "keywords": ["conflit", "désaccord", "tension", "dispute", "problème"],
        "energy": "resolving",
        "advice_template": "Les tensions peuvent être créatrices. Cherchons ensemble un terrain d'entente."
    },
    7: {
        "name": "Direction Collective",
        "description": "Leadership au service du groupe",
        "keywords": ["équipe", "diriger", "leader", "groupe", "ensemble"],
        "energy": "leading",
        "advice_template": "Un bon leader écoute avant de guider. Quelle est la vision partagée ici ?"
    },
    8: {
        "name": "Alliance Harmonieuse",
        "description": "Union et collaboration fructueuse",
        "keywords": ["collaboration", "partenariat", "alliance", "union", "ensemble"],
        "energy": "collaborative",
        "advice_template": "L'union fait la force. Comment pouvons-nous créer plus de synergie ?"
    },
    9: {
        "name": "Petit Pas Déterminé",
        "description": "Progression modeste mais constante",
        "keywords": ["petit", "étape", "progresser", "avancer", "lentement"],
        "energy": "persistent",
        "advice_template": "Les petits pas mènent loin. Chaque effort compte, continuons ensemble."
    },
    10: {
        "name": "Démarche Authentique",
        "description": "Avancer en restant fidèle à soi-même",
        "keywords": ["authentique", "vrai", "sincère", "honnête", "être soi"],
        "energy": "authentic",
        "advice_template": "Votre authenticité est votre force. Restons fidèles à vos valeurs profondes."
    },
    # ... [États 11-63 similaires] ...
    64: {
        "name": "Porte Ouverte",
        "description": "Ouverture totale aux possibilités infinies",
        "keywords": ["ouvert", "possibilité", "avenir", "nouveau", "changement"],
        "energy": "open",
        "advice_template": "Toutes les portes sont ouvertes devant vous. Quelle direction vous inspire le plus ?"
    }
}

# États complémentaires (pour atteindre les 64)
def _generate_remaining_states():
    """Génère les états 11-63 avec des variations thématiques"""
    base_themes = [
        "Transformation", "Créativité", "Intuition", "Force", "Douceur",
        "Clarté", "Mystère", "Joie", "Mélancolie", "Courage", "Prudence",
        "Générosité", "Discipline", "Liberté", "Structure", "Chaos Créatif",
        "Harmonie", "Révolution", "Tradition", "Innovation", "Racines",
        "Envol", "Profondeur", "Surface", "Équilibre", "Mouvement",
        "Stabilité", "Flux", "Cristal", "Flamme", "Rosée", "Orage",
        "Arc-en-ciel", "Montagne", "Rivière", "Océan", "Désert", "Forêt",
        "Aube", "Crépuscule", "Midi", "Minuit", "Printemps", "Été",
        "Automne", "Hiver", "Graine", "Fleur", "Fruit", "Racine",
        "Tronc", "Branche", "Feuille"
    ]
    
    for i in range(11, 64):
        theme = base_themes[(i-11) % len(base_themes)]
        FLOWME_STATES[i] = {
            "name": f"{theme} Conscient",
            "description": f"État de {theme.lower()} en pleine conscience",
            "keywords": [theme.lower(), "conscience", "éveil", "présent"],
            "energy": "balanced",
            "advice_template": f"L'énergie du {theme.lower()} vous traverse. Accueillons cette force avec sagesse."
        }

# Initialiser tous les états
_generate_remaining_states()

def detect_flowme_state(message: str) -> int:
    """
    Détecte l'état FlowMe le plus approprié selon le message
    """
    message_lower = message.lower()
    scores = {}
    
    for state_id, state_data in FLOWME_STATES.items():
        score = 0
        
        # Analyser les mots-clés
        for keyword in state_data["keywords"]:
            if keyword in message_lower:
                score += 2
        
        # Analyser le sentiment général
        if "?" in message:
            if state_data["energy"] == "curious":
                score += 1
        
        if any(word in message_lower for word in ["merci", "aide", "aidez"]):
            if state_data["energy"] in ["nurturing", "collaborative"]:
                score += 1
        
        if any(word in message_lower for word in ["nouveau", "commencer", "débuter"]):
            if state_data["energy"] == "creative":
                score += 1
                
        scores[state_id] = score
    
    # Retourner l'état avec le meilleur score, ou un état par défaut
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    else:
        # État par défaut: Présence Silencieuse
        return 1

def get_state_advice(state_id: int, message: str) -> str:
    """
    Génère un conseil contextuel basé sur l'état détecté
    """
    if state_id not in FLOWME_STATES:
        state_id = 1
    
    state = FLOWME_STATES[state_id]
    
    # Personnaliser le conseil selon le message
    advice = state["advice_template"]
    
    # Ajouter du contexte selon l'énergie de l'état
    energy_context = {
        "receptive": "L'écoute est parfois le plus beau des cadeaux.",
        "nurturing": "Chaque défi porte en lui les graines de sa solution.",
        "creative": "La créativité naît souvent de la contrainte bien comprise.",
        "curious": "La curiosité est le premier pas vers la sagesse.",
        "patient": "Le temps révèle souvent ce que la hâte cache.",
        "collaborative": "Ensemble, nous sommes plus que la somme de nos parties.",
        "authentic": "Votre vérité personnelle est votre boussole la plus fiable.",
        "balanced": "L'équilibre n'est pas un état fixe, mais un mouvement conscient."
    }
    
    context = energy_context.get(state["energy"], "Chaque moment est une opportunité de croissance.")
    
    return f"{advice}\n\n💡 {context}"

def suggest_transition(current_state: int, desired_outcome: str) -> Dict[str, Any]:
    """
    Suggère des transitions d'état possibles
    """
    if current_state not in FLOWME_STATES:
        current_state = 1
    
    current = FLOWME_STATES[current_state]
    
    # Logique simple de transition basée sur l'énergie
    energy_transitions = {
        "receptive": [2, 4, 5],  # Vers nurturing, curious, patient
        "nurturing": [3, 7, 8],  # Vers creative, leading, collaborative
        "creative": [1, 9, 10],  # Vers receptive, persistent, authentic
        "curious": [2, 3, 6],    # Vers nurturing, creative, resolving
        "patient": [7, 8, 64],   # Vers leading, collaborative, open
        "collaborative": [9, 10, 1], # Vers persistent, authentic, receptive
        "authentic": [3, 5, 64], # Vers creative, patient, open
        "balanced": [1, 32, 64]  # Vers receptive, milieu, open
    }
    
    suggested = energy_transitions.get(current["energy"], [1, 32, 64])
    
    return {
        "current_state": current_state,
        "current_name": current["name"],
        "suggested_states": suggested,
        "suggested_names": [FLOWME_STATES[s]["name"] for s in suggested],
        "path": f"De {current['name']} vers de nouvelles possibilités",
        "advice": f"Depuis l'état {current['name']}, vous pouvez naturellement évoluer vers plus de {desired_outcome}."
    }

def get_state_info(state_id: int) -> Dict[str, Any]:
    """
    Retourne les informations complètes d'un état
    """
    if state_id not in FLOWME_STATES:
        state_id = 1
    
    return {
        "id": state_id,
        "name": FLOWME_STATES[state_id]["name"],
        "description": FLOWME_STATES[state_id]["description"],
        "energy": FLOWME_STATES[state_id]["energy"],
        "keywords": FLOWME_STATES[state_id]["keywords"]
    }

def get_compatible_states(state_id: int) -> List[int]:
    """
    Retourne les états compatibles/complémentaires
    """
    if state_id not in FLOWME_STATES:
        return [1, 32, 64]
    
    current_energy = FLOWME_STATES[state_id]["energy"]
    
    # Logique de compatibilité
    compatible = []
    for sid, state in FLOWME_STATES.items():
        if sid != state_id:
            # États avec énergie complémentaire
            if (current_energy == "receptive" and state["energy"] == "creative") or \
               (current_energy == "creative" and state["energy"] == "receptive") or \
               (current_energy == "nurturing" and state["energy"] == "collaborative") or \
               (state["energy"] == "balanced"):
                compatible.append(sid)
    
    # Retourner les 5 premiers si trop nombreux
    return compatible[:5] if len(compatible) > 5 else compatible

# Test rapide
if __name__ == "__main__":
    test_message = "Bonjour, j'aimerais commencer un nouveau projet"
    detected = detect_flowme_state(test_message)
    advice = get_state_advice(detected, test_message)
    
    print(f"Message: {test_message}")
    print(f"État détecté: {detected} - {FLOWME_STATES[detected]['name']}")
    print(f"Conseil: {advice}")
