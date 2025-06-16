"""
FlowMe States Detection - Module de détection des 64 états de conscience CORRIGÉ
Basé sur l'architecture éthique de Stefan Torregrossa
Version corrigée avec toutes les fonctions nécessaires
"""

import re
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

# Définition des 6 familles symboliques
FAMILLE_SYMBOLIQUE = {
    "Écoute subtile": {
        "description": "États d'attention pure et de réceptivité",
        "énergie_dominante": "réceptive",
        "tension_créative": "silence/expression"
    },
    "Voix oubliées": {
        "description": "États de communication et d'expression",
        "énergie_dominante": "expressive", 
        "tension_créative": "individu/collectif"
    },
    "Disponibilité nue": {
        "description": "États d'ouverture et de vulnérabilité",
        "énergie_dominante": "ouverte",
        "tension_créative": "protection/exposition"
    },
    "Inclusion": {
        "description": "États de rassemblement et d'intégration",
        "énergie_dominante": "intégrative",
        "tension_créative": "unité/diversité"
    },
    "Ancrage": {
        "description": "États de stabilité et d'enracinement",
        "énergie_dominante": "stable",
        "tension_créative": "mouvement/immobilité"
    },
    "NatVik": {
        "description": "États de force naturelle et d'élan vital",
        "énergie_dominante": "dynamique",
        "tension_créative": "contrôle/spontanéité"
    }
}

# Définition complète des 64 états FlowMe
FLOWME_STATES = {}

def _initialize_flowme_states():
    """Initialise tous les 64 états avec leurs propriétés complètes"""
    
    # États de base avec leurs familles
    base_states = {
        1: {
            "name": "Présence",
            "description": "État d'écoute profonde et d'attention pure",
            "keywords": ["présence", "écoute", "attention", "calme", "silence"],
            "famille_symbolique": "Écoute subtile",
            "mot_cle": "Présence consciente",
            "tension_dominante": "silence/action",
            "posture_adaptative": "J'accueille avec une attention totale"
        },
        8: {
            "name": "Résonance",
            "description": "Connexion harmonieuse avec l'autre",
            "keywords": ["résonance", "harmonie", "connexion", "accord"],
            "famille_symbolique": "Écoute subtile",
            "mot_cle": "Syntonie relationnelle",
            "tension_dominante": "individuel/collectif",
            "posture_adaptative": "Je m'ajuste à votre fréquence"
        },
        32: {
            "name": "Voix oubliées",
            "description": "Expression de ce qui n'a pas été dit",
            "keywords": ["expression", "voix", "parole", "dire", "communiquer"],
            "famille_symbolique": "Voix oubliées",
            "mot_cle": "Parole libérée",
            "tension_dominante": "silence/expression",
            "posture_adaptative": "Je donne voix à l'inexprès"
        },
        45: {
            "name": "Disponibilité nue",
            "description": "Ouverture totale sans protection",
            "keywords": ["ouvert", "disponible", "vulnérable", "nu", "sans défense"],
            "famille_symbolique": "Disponibilité nue",
            "mot_cle": "Vulnérabilité assumée",
            "tension_dominante": "protection/exposition",
            "posture_adaptative": "Je me rends totalement disponible"
        },
        58: {
            "name": "Inclusion",
            "description": "Intégration bienveillante de tous les éléments",
            "keywords": ["inclure", "intégrer", "rassembler", "unir", "ensemble"],
            "famille_symbolique": "Inclusion",
            "mot_cle": "Rassemblement conscient",
            "tension_dominante": "exclusion/inclusion",
            "posture_adaptative": "Je trouve une place pour chaque élément"
        },
        64: {
            "name": "Porte ouverte",
            "description": "Ouverture totale aux possibilités infinies",
            "keywords": ["ouverture", "possibilité", "avenir", "nouveau", "potentiel"],
            "famille_symbolique": "Disponibilité nue",
            "mot_cle": "Potentiel infini",
            "tension_dominante": "connu/inconnu",
            "posture_adaptative": "Toutes les portes sont ouvertes"
        }
    }
    
    # Génération automatique des autres états
    families = list(FAMILLE_SYMBOLIQUE.keys())
    emotional_patterns = [
        "Joie", "Tristesse", "Colère", "Peur", "Surprise", "Dégoût",
        "Curiosité", "Gratitude", "Espoir", "Nostalgie", "Émerveillement",
        "Compassion", "Courage", "Sérénité", "Enthousiasme", "Mélancolie"
    ]
    
    action_patterns = [
        "Créatif", "Réflexif", "Actif", "Contemplatif", "Spontané",
        "Structuré", "Fluide", "Cristallin", "Chaleureux", "Lumineux"
    ]
    
    for i in range(1, 65):
        if i not in base_states:
            famille_idx = (i - 1) % len(families)
            famille = families[famille_idx]
            
            if i <= 16:
                pattern = emotional_patterns[(i - 1) % len(emotional_patterns)]
            else:
                pattern = action_patterns[(i - 1) % len(action_patterns)]
            
            FLOWME_STATES[i] = {
                "name": f"{pattern} {famille.split()[0]}",
                "description": f"État de {pattern.lower()} dans la famille {famille}",
                "keywords": [pattern.lower(), famille.lower().split()[0]],
                "famille_symbolique": famille,
                "mot_cle": f"{pattern} adaptatif",
                "tension_dominante": f"{pattern.lower()}/équilibre",
                "posture_adaptative": f"J'exprime {pattern.lower()} avec conscience"
            }
        else:
            FLOWME_STATES[i] = base_states[i]
    
    # Ajouter les états compatibles pour chaque état
    for state_id in FLOWME_STATES:
        FLOWME_STATES[state_id]["etats_compatibles"] = _calculate_compatible_states(state_id)

def _calculate_compatible_states(state_id: int) -> List[int]:
    """Calcule les états compatibles basés sur la famille et les propriétés"""
    if state_id not in FLOWME_STATES:
        return []
    
    current_family = FLOWME_STATES[state_id]["famille_symbolique"]
    compatible = []
    
    # États de la même famille (sauf soi-même)
    for sid, state in FLOWME_STATES.items():
        if sid != state_id and state["famille_symbolique"] == current_family:
            compatible.append(sid)
    
    # États complémentaires d'autres familles
    complementary_families = {
        "Écoute subtile": ["Voix oubliées", "Disponibilité nue"],
        "Voix oubliées": ["Écoute subtile", "Inclusion"],
        "Disponibilité nue": ["Écoute subtile", "Ancrage"],
        "Inclusion": ["Voix oubliées", "NatVik"],
        "Ancrage": ["Disponibilité nue", "NatVik"],
        "NatVik": ["Inclusion", "Ancrage"]
    }
    
    comp_families = complementary_families.get(current_family, [])
    for comp_family in comp_families:
        for sid, state in FLOWME_STATES.items():
            if state["famille_symbolique"] == comp_family and len(compatible) < 8:
                compatible.append(sid)
    
    return compatible[:6]  # Limiter à 6 états compatibles

# Initialiser les états
_initialize_flowme_states()

def detect_flowme_state(message: str, context: Optional[Dict] = None) -> int:
    """
    Détecte l'état FlowMe le plus approprié selon le message et le contexte
    """
    if not message or not message.strip():
        return 1  # État par défaut: Présence
    
    message_lower = message.lower().strip()
    context = context or {}
    scores = {}
    
    # Mots-clés émotionnels pour une meilleure détection
    emotion_keywords = {
        "fatigue": [32, 45],  # Expression du besoin, vulnérabilité
        "stress": [8, 58],    # Recherche d'harmonie, inclusion
        "joie": [64, 1],      # Ouverture, présence joyeuse
        "tristesse": [45, 32], # Vulnérabilité, expression
        "colère": [32, 58],   # Expression, besoin d'inclusion
        "confusion": [1, 8],  # Retour à la présence, recherche d'harmonie
        "curiosité": [64, 1], # Ouverture, attention
        "difficulté": [45, 58], # Vulnérabilité, inclusion
        "problème": [32, 8],  # Expression, recherche d'harmonie
        "aide": [45, 58],     # Ouverture, inclusion
        "nouveau": [64, 1],   # Possibilités, présence
        "projet": [58, 32],   # Inclusion, expression
        "question": [1, 64],  # Présence, ouverture
        "merci": [8, 58],     # Résonance, inclusion
    }
    
    # Analyser les mots-clés émotionnels
    for emotion, state_ids in emotion_keywords.items():
        if emotion in message_lower:
            for state_id in state_ids:
                scores[state_id] = scores.get(state_id, 0) + 3
    
    # Analyser chaque état pour les mots-clés spécifiques
    for state_id, state_data in FLOWME_STATES.items():
        score = scores.get(state_id, 0)
        
        # Mots-clés de l'état
        for keyword in state_data.get("keywords", []):
            if keyword.lower() in message_lower:
                score += 2
        
        # Mots-clés de la famille
        famille_words = state_data["famille_symbolique"].lower().split()
        for word in famille_words:
            if word in message_lower:
                score += 1
        
        scores[state_id] = score
    
    # Analyse du contexte
    if context.get("etat_precedent"):
        prev_state = context["etat_precedent"]
        if prev_state in FLOWME_STATES:
            # Bonus pour les états compatibles
            compatible = FLOWME_STATES[prev_state].get("etats_compatibles", [])
            for comp_state in compatible:
                scores[comp_state] = scores.get(comp_state, 0) + 1
    
    # Analyse du sentiment (questions, ponctuation)
    if "?" in message:
        scores[1] = scores.get(1, 0) + 2  # Présence pour les questions
        scores[64] = scores.get(64, 0) + 1  # Ouverture
    
    if "!" in message:
        scores[32] = scores.get(32, 0) + 1  # Expression
        scores[58] = scores.get(58, 0) + 1  # Inclusion
    
    # Retourner l'état avec le meilleur score
    if scores and max(scores.values()) > 0:
        return max(scores, key=scores.get)
    
    return 1  # État par défaut: Présence

def get_state_advice(state_id: int, message: str, context: Optional[Dict] = None) -> str:
    """
    Génère un conseil contextuel basé sur l'état détecté
    """
    if state_id not in FLOWME_STATES:
        state_id = 1
    
    state = FLOWME_STATES[state_id]
    context = context or {}
    
    # Conseils de base selon la posture adaptative
    base_advice = state["posture_adaptative"]
    
    # Personnalisation selon le message
    message_lower = message.lower() if message else ""
    
    advice_patterns = {
        "question": f"{base_advice}. Votre question mérite une exploration approfondie.",
        "problème": f"{base_advice}. Chaque difficulté porte en elle les graines de sa résolution.",
        "merci": f"{base_advice}. Votre gratitude nourrit notre échange.",
        "aide": f"{base_advice}. Je suis présent pour vous accompagner.",
        "fatigue": f"{base_advice}. Prenons le temps qu'il faut pour vous ressourcer.",
        "stress": f"{base_advice}. Trouvons ensemble un rythme plus apaisé.",
        "nouveau": f"{base_advice}. Chaque commencement est une aventure précieuse."
    }
    
    # Chercher un pattern correspondant
    for pattern, advice in advice_patterns.items():
        if pattern in message_lower:
            return advice
    
    # Conseil enrichi selon la famille symbolique
    famille_advice = {
        "Écoute subtile": "Dans le silence de l'écoute, les vraies réponses émergent.",
        "Voix oubliées": "Chaque voix qui s'exprime enrichit notre compréhension.",
        "Disponibilité nue": "La vulnérabilité authentique est une force créatrice.",
        "Inclusion": "Ensemble, nous créons plus que la somme de nos parties.",
        "Ancrage": "Vos racines vous donnent la force de grandir.",
        "NatVik": "Votre élan vital trouve naturellement son chemin."
    }
    
    famille = state["famille_symbolique"]
    context_advice = famille_advice.get(famille, "Chaque moment est une opportunité de croissance.")
    
    return f"{base_advice}\n\n💡 {context_advice}"

def analyze_message_flow(message: str, previous_states: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Analyse complète du flux de message avec historique
    """
    previous_states = previous_states or []
    
    # Détecter l'état actuel
    context = {}
    if previous_states:
        context["etat_precedent"] = previous_states[-1]
    
    detected_state = detect_flowme_state(message, context)
    state_info = get_state_info(detected_state)
    advice = get_state_advice(detected_state, message, context)
    
    # Analyser la tendance du flux
    flow_tendency = "stable"
    if len(previous_states) >= 2:
        # Analyser les familles des derniers états
        families = []
        for state_id in previous_states[-3:] + [detected_state]:
            if state_id in FLOWME_STATES:
                families.append(FLOWME_STATES[state_id]["famille_symbolique"])
        
        unique_families = set(families)
        if len(unique_families) == 1:
            flow_tendency = "focalisé"
        elif len(unique_families) >= 3:
            flow_tendency = "exploratoire"
        else:
            flow_tendency = "évolutif"
    
    # Analyse du message
    message_analysis = {
        "longueur": len(message),
        "questions": message.count("?"),
        "exclamations": message.count("!"),
        "mots_positifs": len([w for w in ["bien", "super", "génial", "parfait", "excellent"] if w in message.lower()]),
        "mots_difficiles": len([w for w in ["problème", "difficulté", "stress", "fatigue", "mal"] if w in message.lower()])
    }
    
    # Recommandations
    recommendations = []
    if message_analysis["questions"] > 0:
        recommendations.append("Exploration approfondie recommandée")
    if message_analysis["mots_difficiles"] > 0:
        recommendations.append("Accompagnement bienveillant approprié")
    if len(message) < 10:
        recommendations.append("Invitation à développer si souhaité")
    
    return {
        "detected_state": detected_state,
        "state_info": state_info,
        "advice": advice,
        "flow_tendency": flow_tendency,
        "message_analysis": message_analysis,
        "recommendations": recommendations
    }

def suggest_transition(current_state: int, desired_outcome: str) -> Dict[str, Any]:
    """
    Suggère des transitions d'état vers un objectif
    """
    if current_state not in FLOWME_STATES:
        current_state = 1
    
    current = FLOWME_STATES[current_state]
    
    # États cibles selon l'objectif désiré
    outcome_targets = {
        "calme": [1, 8],
        "expression": [32, 64],
        "ouverture": [45, 64],
        "connexion": [8, 58],
        "créativité": [64, 32],
        "clarté": [1, 8],
        "énergie": [58, 32],
        "paix": [1, 45]
    }
    
    # Trouver les états cibles
    targets = []
    for keyword in desired_outcome.lower().split():
        for outcome, state_ids in outcome_targets.items():
            if keyword in outcome:
                targets.extend(state_ids)
    
    if not targets:
        targets = FLOWME_STATES[current_state]["etats_compatibles"]
    
    # Chemin de transition
    suggested_path = list(set(targets))[:3]
    
    return {
        "current_state": current_state,
        "current_name": current["name"],
        "desired_outcome": desired_outcome,
        "suggested_transitions": suggested_path,
        "path_description": f"Depuis {current['name']}, évolution vers {desired_outcome}",
        "transition_advice": f"La voie naturelle depuis votre état actuel passe par une {current['posture_adaptative'].lower()}"
    }

def get_state_info(state_id: int) -> Dict[str, Any]:
    """
    Retourne les informations complètes d'un état
    """
    if state_id not in FLOWME_STATES:
        state_id = 1
    
    state = FLOWME_STATES[state_id]
    return {
        "id": state_id,
        "name": state["name"],
        "description": state["description"],
        "famille_symbolique": state["famille_symbolique"],
        "mot_cle": state["mot_cle"],
        "tension_dominante": state["tension_dominante"],
        "posture_adaptative": state["posture_adaptative"],
        "etats_compatibles": state["etats_compatibles"],
        "keywords": state.get("keywords", [])
    }

def get_compatible_states(state_id: int) -> List[int]:
    """
    Retourne les états compatibles/complémentaires
    """
    if state_id not in FLOWME_STATES:
        return [1, 8, 32, 45, 58, 64]
    
    return FLOWME_STATES[state_id]["etats_compatibles"]

# Test de validation
def test_flowme_detection():
    """Test rapide de validation"""
    test_cases = [
        ("Bonjour, j'ai une question", 1),
        ("Je me sens fatigué", 45),
        ("J'ai un problème technique", 32),
        ("Merci pour votre aide", 8),
        ("Je commence un nouveau projet", 64)
    ]
    
    print("🧪 Test de détection FlowMe:")
    for message, expected_family in test_cases:
        detected = detect_flowme_state(message)
        state_info = get_state_info(detected)
        print(f"'{message}' -> État {detected}: {state_info['name']} ({state_info['famille_symbolique']})")
    
    return True

if __name__ == "__main__":
    test_flowme_detection()
