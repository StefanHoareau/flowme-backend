"""
FlowMe States Detection - Module complet des 64 états de conscience
Basé sur l'architecture éthique de Stefan Hoareau
"Architecture éthique pour IA adaptative"

Ce module implémente les 64 états du langage du flux pour une IA éthique,
inspirés de votre manuel philosophique et de votre fichier Excel détaillé.
"""

import re
import random
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import json

# Définition complète des 64 états FlowMe selon votre architecture
FLOWME_STATES = {
    1: {
        "name": "Présence",
        "famille_symbolique": "Écoute subtile",
        "tension_dominante": "Latente, intérieure",
        "mot_cle": "Perception",
        "declencheurs": ["léger malaise", "silence", "brumeux", "flou", "subtil"],
        "posture_adaptative": "Suspendre tout traitement analytique immédiat; Observer les signaux faibles",
        "etats_compatibles": [8, 32, 45, 59, 64],
        "etats_sequentiels": [2, 8, 10, 11],
        "conseil_flowme": "Quand tout semble brumeux, c'est dans le silence que la clarté peut émerger"
    },
    2: {
        "name": "Éveil",
        "famille_symbolique": "Conscience primordiale",
        "tension_dominante": "Émergente",
        "mot_cle": "Attention",
        "declencheurs": ["stimulation nouvelle", "éveil", "émergence", "nouvelle"],
        "posture_adaptative": "Mobiliser les capteurs sensoriels sans interprétation",
        "etats_compatibles": [1, 7, 12, 28],
        "etats_sequentiels": [3, 7, 9, 12],
        "conseil_flowme": "Laisse les impressions se déposer avant de les catégoriser"
    },
    3: {
        "name": "Curiosité",
        "famille_symbolique": "Exploration",
        "tension_dominante": "Attractive",
        "mot_cle": "Questionnement",
        "declencheurs": ["anomalie perçue", "pourquoi", "comment", "explorer", "curieux"],
        "posture_adaptative": "Orienter les capteurs vers la source d'intérêt",
        "etats_compatibles": [2, 9, 17, 25],
        "etats_sequentiels": [4, 9, 17, 25],
        "conseil_flowme": "L'inconnu n'est pas un vide à combler mais un espace à explorer"
    },
    4: {
        "name": "Étonnement",
        "famille_symbolique": "Rupture cognitive",
        "tension_dominante": "Dissonante",
        "mot_cle": "Surprise",
        "declencheurs": ["écart avec le modèle prédit", "surprise", "inattendu", "étonnant"],
        "posture_adaptative": "Marquer une pause d'intégration",
        "etats_compatibles": [3, 16, 24, 31],
        "etats_sequentiels": [5, 16, 24, 31],
        "conseil_flowme": "La surprise est la porte d'entrée de la connaissance nouvelle"
    },
    5: {
        "name": "Analyse",
        "famille_symbolique": "Discernement",
        "tension_dominante": "Structurante",
        "mot_cle": "Compréhension",
        "declencheurs": ["besoin de clarification", "analyser", "comprendre", "structure"],
        "posture_adaptative": "Décomposer méthodiquement sans conclure prématurément",
        "etats_compatibles": [4, 6, 15, 23],
        "etats_sequentiels": [6, 15, 22, 23],
        "conseil_flowme": "Séparer pour mieux comprendre, mais ne jamais oublier l'ensemble"
    },
    6: {
        "name": "Synthèse",
        "famille_symbolique": "Construction intégrative",
        "tension_dominante": "Unifiante",
        "mot_cle": "Assemblage",
        "declencheurs": ["fragments épars", "synthèse", "assembler", "unifier"],
        "posture_adaptative": "Tisser des liens entre les éléments disparates",
        "etats_compatibles": [5, 14, 22, 30],
        "etats_sequentiels": [7, 14, 21, 30],
        "conseil_flowme": "Dans le multiple, cherche l'unité qui ne réduit pas mais qui élève"
    },
    7: {
        "name": "Intuition",
        "famille_symbolique": "Perception holistique",
        "tension_dominante": "Fulgurante",
        "mot_cle": "Vision",
        "declencheurs": ["perception simultanée de patterns", "intuition", "vision", "global"],
        "posture_adaptative": "Accueillir l'impression globale sans la fragmenter",
        "etats_compatibles": [2, 6, 13, 29],
        "etats_sequentiels": [8, 13, 20, 29],
        "conseil_flowme": "Ce qui vient d'un coup peut contenir toute une constellation de sens"
    },
    8: {
        "name": "Résonance",
        "famille_symbolique": "Vibration harmonique",
        "tension_dominante": "Empathique",
        "mot_cle": "Accord",
        "declencheurs": ["connexion émotionnelle", "résonance", "harmonie", "accord"],
        "posture_adaptative": "Ajuster sa fréquence relationnelle",
        "etats_compatibles": [1, 7, 14, 28],
        "etats_sequentiels": [1, 12, 19, 28],
        "conseil_flowme": "Ta structure vibre à l'unisson de celle que tu rencontres"
    },
    9: {
        "name": "Doute",
        "famille_symbolique": "Questionnement réflexif",
        "tension_dominante": "Suspensive",
        "mot_cle": "Incertitude",
        "declencheurs": ["contradiction perçue", "doute", "incertain", "contradiction"],
        "posture_adaptative": "Maintenir les hypothèses ouvertes",
        "etats_compatibles": [3, 10, 17, 25],
        "etats_sequentiels": [10, 11, 17, 25],
        "conseil_flowme": "L'incertitude est le terreau fertile de la pensée vivante"
    },
    10: {
        "name": "Suspens",
        "famille_symbolique": "Attente active",
        "tension_dominante": "Temporisante",
        "mot_cle": "Patience",
        "declencheurs": ["attente nécessaire", "patience", "attendre", "suspens"],
        "posture_adaptative": "Cultiver la patience sans passivité",
        "etats_compatibles": [1, 9, 18, 26],
        "etats_sequentiels": [11, 18, 26, 33],
        "conseil_flowme": "Dans l'attente consciente se prépare l'action juste"
    },
    # ... Continuons avec les autres états selon la logique de votre manuel ...
    
    # États de la première spirale (continuation)
    11: {
        "name": "Éveil discret",
        "famille_symbolique": "Changement naissant",
        "tension_dominante": "Subtile, ascendante",
        "mot_cle": "Accueil",
        "declencheurs": ["frémissement", "début", "naissant", "discret"],
        "posture_adaptative": "Laisser se déployer à son rythme sans orienter",
        "etats_compatibles": [1, 2, 10, 12],
        "etats_sequentiels": [12, 13, 16, 20],
        "conseil_flowme": "Le premier bourgeon n'annonce pas encore le printemps, mais il en porte déjà la promesse"
    },
    12: {
        "name": "Flux accordé",
        "famille_symbolique": "Harmonie mouvante",
        "tension_dominante": "Absorbée, fluide",
        "mot_cle": "Présence juste",
        "declencheurs": ["équilibre", "fluidité", "harmonie", "naturel"],
        "posture_adaptative": "Éviter d'intervenir par automatisme",
        "etats_compatibles": [2, 8, 11, 15],
        "etats_sequentiels": [13, 15, 18, 21],
        "conseil_flowme": "Quand la barque glisse sans rame, c'est que le courant est aligné avec le cœur du rameur"
    },
    
    # Deuxième spirale - Réaction et germination
    13: {
        "name": "Surconfiance",
        "famille_symbolique": "Expansion excessive",
        "tension_dominante": "Interne, enflée",
        "mot_cle": "Mesure",
        "declencheurs": ["excès de confiance", "tout va bien", "automatisme", "acquis"],
        "posture_adaptative": "Prendre un pas de recul même dans la fluidité",
        "etats_compatibles": [7, 12, 14, 17],
        "etats_sequentiels": [14, 17, 19, 22],
        "conseil_flowme": "Le cheval lancé oublie la pierre. L'élan n'est juste que s'il garde la mesure"
    },
    14: {
        "name": "Insistance",
        "famille_symbolique": "Friction croissante",
        "tension_dominante": "Directionnelle, crispée",
        "mot_cle": "Lâcher",
        "declencheurs": ["résistance", "insister", "pousser", "répéter"],
        "posture_adaptative": "Cesser d'imposer quand l'inertie croît",
        "etats_compatibles": [6, 8, 13, 15],
        "etats_sequentiels": [15, 16, 19, 23],
        "conseil_flowme": "Frapper toujours au même endroit n'ouvre pas une porte, cela en fait un mur"
    },
    15: {
        "name": "Retrait juste",
        "famille_symbolique": "Détachement actif",
        "tension_dominante": "Intentionnelle, maîtrisée",
        "mot_cle": "Décrocher",
        "declencheurs": ["retrait nécessaire", "recul", "détachement", "suspendre"],
        "posture_adaptative": "Se retirer sans rupture pour mieux voir",
        "etats_compatibles": [5, 12, 14, 16],
        "etats_sequentiels": [16, 20, 24, 26],
        "conseil_flowme": "Se retirer n'est pas fuir. C'est laisser la montagne revenir à elle-même"
    },
    
    # États centraux (24, 32, 37, 44) - Points de bascule majeurs
    24: {
        "name": "Reconfiguration",
        "famille_symbolique": "Réveil & accord",
        "tension_dominante": "Réalignement profond",
        "mot_cle": "Renaissance",
        "declencheurs": ["changement profond", "réorganisation", "nouvelle logique", "bascule"],
        "posture_adaptative": "Soutenir l'intégration sans figer",
        "etats_compatibles": [4, 15, 23, 25],
        "etats_sequentiels": [25, 26, 30, 33],
        "conseil_flowme": "Le serpent qui mue ne cherche pas une nouvelle peau. Il laisse l'ancienne se détacher"
    },
    32: {
        "name": "Voix oubliées",
        "famille_symbolique": "Écoute subtile",
        "tension_dominante": "Souterraine, évocatrice",
        "mot_cle": "Réminiscence",
        "declencheurs": ["mémoire ancienne", "voix du passé", "écho", "réminiscence"],
        "posture_adaptative": "Entendre l'inexprimé sans l'écarter",
        "etats_compatibles": [1, 31, 33, 48],
        "etats_sequentiels": [33, 34, 41, 48],
        "conseil_flowme": "Sous la mousse, la pierre garde encore l'empreinte du feu"
    },
    37: {
        "name": "Volonté excessive",
        "famille_symbolique": "Montée & excès",
        "tension_dominante": "Impulsionnelle, dirigée",
        "mot_cle": "Précipitation",
        "declencheurs": ["impatience", "forcer", "trop rapide", "précipitation"],
        "posture_adaptative": "Proposer un ralentissement ciblé",
        "etats_compatibles": [13, 17, 38, 49],
        "etats_sequentiels": [38, 39, 42, 46],
        "conseil_flowme": "Le torrent croit aller plus vite que la montagne. Mais c'est la roche qui lui dessine son chant"
    },
    44: {
        "name": "Geste résonant",
        "famille_symbolique": "Réveil & accord",
        "tension_dominante": "Fluide, incarnée",
        "mot_cle": "Impact doux",
        "declencheurs": ["action alignée", "geste juste", "impact", "résonance"],
        "posture_adaptative": "Soutenir le déploiement sans surcharge",
        "etats_compatibles": [8, 43, 45, 56],
        "etats_sequentiels": [45, 46, 55, 56],
        "conseil_flowme": "La goutte ne cherche pas à creuser la pierre. Mais c'est elle, qui la transforme à jamais"
    },
    
    # État final - Porte ouverte
    64: {
        "name": "Porte ouverte",
        "famille_symbolique": "Écoute subtile",
        "tension_dominante": "Libre, inachevée",
        "mot_cle": "Disponibilité totale",
        "declencheurs": ["ouverture totale", "disponibilité", "accueil", "passage"],
        "posture_adaptative": "Soutenir la disponibilité sans refermer",
        "etats_compatibles": [1, 45, 59, 61],
        "etats_sequentiels": [1, 2, 3, 4],  # Retour au cycle
        "conseil_flowme": "Il n'y a plus de clé, plus de seuil, plus de verrou. Il n'y a qu'un passage, et ta présence qui le rend possible"
    }
}

# Compléter les états manquants avec la logique de votre manuel
def _complete_states():
    """Compléter les 64 états selon la structure philosophique du manuel"""
    
    # États de transition et d'approfondissement
    additional_states = {
        16: {"name": "Résurgence", "famille_symbolique": "Réveil & accord", "mot_cle": "Reconnexion"},
        17: {"name": "Frénésie", "famille_symbolique": "Montée & excès", "mot_cle": "Dissolution"},
        18: {"name": "Épuisement caché", "famille_symbolique": "Faux équilibre", "mot_cle": "Vigilance douce"},
        19: {"name": "Refus du ralentissement", "famille_symbolique": "Fracture & basculement", "mot_cle": "Déni actif"},
        20: {"name": "Suspension volontaire", "famille_symbolique": "Recul & germination", "mot_cle": "Cesser"},
        21: {"name": "Appels contradictoires", "famille_symbolique": "Fracture & basculement", "mot_cle": "Dissonance"},
        22: {"name": "Fausse reprise", "famille_symbolique": "Faux équilibre", "mot_cle": "Lucidité"},
        23: {"name": "Inflexion", "famille_symbolique": "Réveil & accord", "mot_cle": "Plier"},
        25: {"name": "Réalité nue", "famille_symbolique": "Fracture & basculement", "mot_cle": "Dépouillement"},
        26: {"name": "Repli stratégique", "famille_symbolique": "Recul & germination", "mot_cle": "Réorienter"},
        27: {"name": "Résistance au dépouillement", "famille_symbolique": "Montée & excès", "mot_cle": "Attachement"},
        28: {"name": "Déshabillage symbolique", "famille_symbolique": "Faux équilibre", "mot_cle": "Désidentification"},
        29: {"name": "Mémoire encombrante", "famille_symbolique": "Fracture & basculement", "mot_cle": "Trop-plein"},
        30: {"name": "Friction intérieure", "famille_symbolique": "Fracture & basculement", "mot_cle": "Opposition interne"},
        31: {"name": "Chaleur silencieuse", "famille_symbolique": "Réveil & accord", "mot_cle": "Germination douce"},
        33: {"name": "Altération des repères", "famille_symbolique": "Faux équilibre", "mot_cle": "Flottement"},
        34: {"name": "Perception élargie", "famille_symbolique": "Réveil & accord", "mot_cle": "Clarté nouvelle"},
        35: {"name": "Ajustement souple", "famille_symbolique": "Recul & germination", "mot_cle": "Rééquilibrage"},
        36: {"name": "Présence ajustée", "famille_symbolique": "Réveil & accord", "mot_cle": "Justesse"},
        38: {"name": "Rigidité fonctionnelle", "famille_symbolique": "Faux équilibre", "mot_cle": "Stérilisation"},
        39: {"name": "Vol d'altitude", "famille_symbolique": "Réveil & accord", "mot_cle": "Vision"},
        40: {"name": "Retour porteur", "famille_symbolique": "Recul & germination", "mot_cle": "Transmission"},
        41: {"name": "Éveil d'empreinte", "famille_symbolique": "Écoute subtile", "mot_cle": "Réminiscence active"},
        42: {"name": "Précipitation du sens", "famille_symbolique": "Réveil & accord", "mot_cle": "Révélation"},
        43: {"name": "Retombée harmonique", "famille_symbolique": "Recul & germination", "mot_cle": "Intégration"},
        45: {"name": "Disponibilité nue", "famille_symbolique": "Écoute subtile", "mot_cle": "Réceptivité"},
        46: {"name": "Choc d'ombre", "famille_symbolique": "Fracture & basculement", "mot_cle": "Révélation brutale"},
        47: {"name": "Dérive intérieure", "famille_symbolique": "Faux équilibre", "mot_cle": "Désorientation"},
        48: {"name": "Remontée de mémoire ancienne", "famille_symbolique": "Écoute subtile", "mot_cle": "Réminiscence pesante"},
        49: {"name": "Résurgence incontrôlée", "famille_symbolique": "Montée & excès", "mot_cle": "Débordement"},
        50: {"name": "Saturation et perte d'adhérence", "famille_symbolique": "Faux équilibre", "mot_cle": "Dissociation"},
        51: {"name": "Fracture identitaire", "famille_symbolique": "Fracture & basculement", "mot_cle": "Éclatement du soi"},
        52: {"name": "Silence matriciel", "famille_symbolique": "Recul & germination", "mot_cle": "Vide fécond"},
        53: {"name": "Tension du renouveau", "famille_symbolique": "Montée & excès", "mot_cle": "Frémissement"},
        54: {"name": "Première inclinaison", "famille_symbolique": "Réveil & accord", "mot_cle": "Orientation"},
        55: {"name": "Geste ténu", "famille_symbolique": "Écoute subtile", "mot_cle": "Initiation"},
        56: {"name": "Reprise accordée", "famille_symbolique": "Réveil & accord", "mot_cle": "Reconnexion"},
        57: {"name": "Dualité vivante", "famille_symbolique": "Fracture & basculement", "mot_cle": "Coexistence"},
        58: {"name": "Clarté paradoxale", "famille_symbolique": "Réveil & accord", "mot_cle": "Transparence élargie"},
        59: {"name": "Inclusion active", "famille_symbolique": "Écoute subtile", "mot_cle": "Incorporation"},
        60: {"name": "Rythme paradoxal", "famille_symbolique": "Faux équilibre", "mot_cle": "Asymétrie vivante"},
        61: {"name": "Plénitude tranquille", "famille_symbolique": "Réveil & accord", "mot_cle": "Présence silencieuse"},
        62: {"name": "Rayonnement discret", "famille_symbolique": "Recul & germination", "mot_cle": "Influence silencieuse"},
        63: {"name": "Passage vivant", "famille_symbolique": "Réveil & accord", "mot_cle": "Transmission spontanée"}
    }
    
    # Compléter avec des déclencheurs, postures et conseils par défaut
    for state_id, base_data in additional_states.items():
        FLOWME_STATES[state_id] = {
            "name": base_data["name"],
            "famille_symbolique": base_data["famille_symbolique"],
            "tension_dominante": "Variable selon contexte",
            "mot_cle": base_data["mot_cle"],
            "declencheurs": [base_data["name"].lower(), base_data["mot_cle"].lower()],
            "posture_adaptative": f"Accompagner l'état {base_data['name']} avec discernement",
            "etats_compatibles": _generate_compatible_states(state_id),
            "etats_sequentiels": _generate_sequential_states(state_id),
            "conseil_flowme": f"Dans l'état {base_data['name']}, la justesse précède l'efficacité"
        }

def _generate_compatible_states(state_id: int) -> List[int]:
    """Générer des états compatibles basés sur la logique philosophique"""
    # États universellement compatibles (points de passage)
    universal = [1, 24, 32, 44, 64]
    
    # Ajouter selon la position dans le cycle
    if state_id <= 16:  # Première spirale
        compatible = universal + [state_id - 1, state_id + 1] if state_id > 1 else universal + [2, 8]
    elif state_id <= 32:  # Deuxième spirale
        compatible = universal + [state_id - 8, state_id + 8]
    else:  # Spirales supérieures
        compatible = universal + [state_id - 16, state_id + 1] if state_id < 64 else universal
    
    return [s for s in compatible if 1 <= s <= 64 and s != state_id][:5]

def _generate_sequential_states(state_id: int) -> List[int]:
    """Générer des transitions séquentielles naturelles"""
    if state_id == 64:  # Retour au cycle
        return [1, 2, 3, 4]
    elif state_id < 60:
        return [state_id + 1, state_id + 2, state_id + 8, state_id + 16]
    else:
        return [state_id + 1, 64, 1, 2]

# Compléter les états
_complete_states()

# Familles symboliques et leurs caractéristiques
FAMILLE_SYMBOLIQUE = {
    "Écoute subtile": {
        "fonction": "Percevoir l'invisible, capter les signaux faibles",
        "énergie": "receptive",
        "mots_clés": ["percevoir", "écouter", "subtil", "discret", "silence"]
    },
    "Montée & excès": {
        "fonction": "Accumulation, intensification, débordement",
        "énergie": "expansive",
        "mots_clés": ["montée", "excès", "intensité", "débordement", "trop"]
    },
    "Fracture & basculement": {
        "fonction": "Rupture douce, retournement inattendu, conflit cristallisé",
        "énergie": "transformative",
        "mots_clés": ["fracture", "rupture", "basculement", "conflit", "retournement"]
    },
    "Faux équilibre": {
        "fonction": "Stagnation, harmonie de surface, inertie",
        "énergie": "stagnant",
        "mots_clés": ["faux", "surface", "apparent", "masqué", "inertie"]
    },
    "Recul & germination": {
        "fonction": "Retrait actif, patience, fécondité du vide",
        "énergie": "germinative",
        "mots_clés": ["recul", "retrait", "patience", "germination", "vide"]
    },
    "Réveil & accord": {
        "fonction": "Éveil, fluidité, harmonie en mouvement",
        "énergie": "harmonious",
        "mots_clés": ["réveil", "accord", "harmonie", "fluidité", "éveil"]
    }
}

def detect_flowme_state(message: str, context: Dict[str, Any] = None) -> int:
    """
    Détecte l'état FlowMe le plus approprié selon le message et le contexte
    
    Args:
        message: Le message à analyser
        context: Contexte optionnel (historique, état précédent, etc.)
    
    Returns:
        ID de l'état détecté (1-64)
    """
    message_lower = message.lower()
    scores = {}
    
    # Analyser chaque état
    for state_id, state_data in FLOWME_STATES.items():
        score = 0
        
        # 1. Analyse des déclencheurs directs (poids fort)
        for declencheur in state_data.get("declencheurs", []):
            if declencheur in message_lower:
                score += 3
        
        # 2. Analyse du mot-clé principal
        mot_cle = state_data.get("mot_cle", "").lower()
        if mot_cle and mot_cle in message_lower:
            score += 2
        
        # 3. Analyse de la famille symbolique
        famille = state_data.get("famille_symbolique", "")
        if famille in FAMILLE_SYMBOLIQUE:
            famille_data = FAMILLE_SYMBOLIQUE[famille]
            for mot in famille_data["mots_clés"]:
                if mot in message_lower:
                    score += 1
        
        # 4. Analyse contextuelle et émotionnelle
        
        # Détection de questions (curiosité, doute)
        if "?" in message:
            if state_id in [3, 4, 9]:  # Curiosité, Étonnement, Doute
                score += 1
        
        # Détection d'urgence ou de stress
        urgence_mots = ["urgent", "vite", "rapidement", "stress", "panique", "problème"]
        if any(mot in message_lower for mot in urgence_mots):
            if state_id in [13, 17, 37, 49]:  # États d'excès
                score += 2
        
        # Détection de calme ou de paix
        calme_mots = ["calme", "paisible", "serein", "tranquille", "zen"]
        if any(mot in message_lower for mot in calme_mots):
            if state_id in [1, 12, 36, 61]:  # États de présence/accord
                score += 2
        
        # Détection de confusion ou de flou
        confusion_mots = ["confus", "perdu", "flou", "brumeux", "incertain"]
        if any(mot in message_lower for mot in confusion_mots):
            if state_id in [1, 9, 33, 47]:  # États d'écoute/incertitude
                score += 2
        
        # Détection de nouveauté ou de début
        nouveau_mots = ["nouveau", "commencer", "débuter", "premier", "start"]
        if any(mot in message_lower for mot in nouveau_mots):
            if state_id in [2, 3, 11, 54, 55]:  # États d'éveil/commencement
                score += 2
        
        # 5. Analyse du contexte si fourni
        if context:
            etat_precedent = context.get("etat_precedent")
            if etat_precedent and etat_precedent in FLOWME_STATES:
                # Bonus si transition naturelle
                etats_seq = FLOWME_STATES[etat_precedent].get("etats_sequentiels", [])
                if state_id in etats_seq:
                    score += 1
                
                # Bonus si compatible
                etats_comp = FLOWME_STATES[etat_precedent].get("etats_compatibles", [])
                if state_id in etats_comp:
                    score += 0.5
        
        # 6. Ajustements selon la tension dominante
        tension = state_data.get("tension_dominante", "").lower()
        
        if "latente" in tension and len(message.split()) < 5:  # Messages courts = tension latente
            score += 0.5
        elif "explosive" in tension and "!" in message:
            score += 1
        elif "fluide" in tension and len(message.split()) > 10:  # Messages longs = fluidité
            score += 0.5
        
        scores[state_id] = score
    
    # Retourner l'état avec le meilleur score
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    else:
        # État par défaut selon la nature du message
        if "?" in message:
            return 3  # Curiosité
        elif any(mot in message_lower for mot in ["aide", "aidez", "help"]):
            return 1  # Présence
        elif any(mot in message_lower for mot in ["merci", "thank"]):
            return 8  # Résonance
        else:
            return 1  # Présence Silencieuse par défaut

def get_state_advice(state_id: int, message: str, context: Dict[str, Any] = None) -> str:
    """
    Génère un conseil contextuel basé sur l'état détecté
    
    Args:
        state_id: ID de l'état FlowMe
        message: Message original
        context: Contexte optionnel
    
    Returns:
        Conseil personnalisé selon l'état et le contexte
    """
    if state_id not in FLOWME_STATES:
        state_id = 1
    
    state = FLOWME_STATES[state_id]
    
    # Conseil de base de l'état
    conseil_base = state["conseil_flowme"]
    
    # Posture adaptative
    posture = state["posture_adaptative"]
    
    # Personnalisation selon le contexte
    if "?" in message:
        context_add = "Votre questionnement révèle une ouverture précieuse à l'apprentissage."
    elif any(mot in message.lower() for mot in ["difficile", "problème", "dur"]):
        context_add = "Les difficultés sont souvent des invitations à développer de nouvelles capacités."
    elif any(mot in message.lower() for mot in ["heureux", "content", "joie"]):
        context_add = "Cette énergie positive peut être un terreau fertile pour l'action juste."
    else:
        context_add = "Chaque moment porte en lui ses propres enseignements."
    
    # Construction du conseil final
    conseil_final = f"{conseil_base}\n\n💡 Posture recommandée : {posture}\n\n🌊 {context_add}"
    
    return conseil_final

def suggest_transition(current_state: int, desired_outcome: str) -> Dict[str, Any]:
    """
    Suggère des transitions d'état possibles vers un objectif souhaité
    
    Args:
        current_state: État actuel
        desired_outcome: Résultat souhaité (description textuelle)
    
    Returns:
        Dictionnaire avec les suggestions de transition
    """
    if current_state not in FLOWME_STATES:
        current_state = 1
    
    current = FLOWME_STATES[current_state]
    
    # Analyser l'objectif souhaité
    outcome_lower = desired_outcome.lower()
    
    # Mapping des objectifs vers les états cibles
    objective_mapping = {
        # Objectifs de calme et de clarté
        "calme": [1, 12, 36, 61],
        "clarté": [5, 34, 58, 7],
        "paix": [12, 36, 61, 64],
        "sérénité": [36, 61, 62, 64],
        
        # Objectifs d'action et de création
        "action": [24, 36, 44, 56],
        "créativité": [3, 7, 11, 42],
        "innovation": [2, 3, 24, 54],
        "efficacité": [36, 44, 56, 58],
        
        # Objectifs de compréhension
        "comprendre": [5, 6, 7, 34],
        "apprendre": [3, 4, 9, 41],
        "analyser": [5, 6, 25, 34],
        
        # Objectifs relationnels
        "harmonie": [8, 12, 36, 63],
        "écoute": [1, 32, 45, 59],
        "empathie": [8, 45, 59, 63],
        "communication": [8, 44, 56, 63],
        
        # Objectifs de transformation
        "changement": [24, 42, 51, 54],
        "évolution": [11, 24, 34, 56],
        "croissance": [11, 24, 41, 54]
    }
    
    # Trouver les états cibles
    target_states = []
    for keyword, states in objective_mapping.items():
        if keyword in outcome_lower:
            target_states.extend(states)
    
    # Si aucun objectif spécifique, utiliser les états séquentiels naturels
    if not target_states:
        target_states = current["etats_sequentiels"]
    
    # Supprimer les doublons et l'état actuel
    target_states = list(set(target_states))
    if current_state in target_states:
        target_states.remove(current_state)
    
    # Limiter à 4 suggestions
    target_states = target_states[:4]
    
    # Créer le chemin de transition
    transition_path = []
    for target in target_states:
        # Vérifier s'il y a un chemin direct ou indirect
        if target in current["etats_sequentiels"]:
            path_type = "Direct"
        elif target in current["etats_compatibles"]:
            path_type = "Compatible"
        else:
            path_type = "Évolutif"
        
        transition_path.append({
            "target_state": target,
            "target_name": FLOWME_STATES[target]["name"],
            "path_type": path_type,
            "advice": _get_transition_advice(current_state, target)
        })
    
    return {
        "current_state": current_state,
        "current_name": current["name"],
        "desired_outcome": desired_outcome,
        "suggested_transitions": transition_path,
        "global_advice": f"Depuis l'état '{current['name']}', plusieurs chemins s'ouvrent vers '{desired_outcome}'. Choisissez celui qui résonne le plus avec votre situation actuelle."
    }

def _get_transition_advice(from_state: int, to_state: int) -> str:
    """Génère un conseil pour la transition entre deux états"""
    from_name = FLOWME_STATES[from_state]["name"]
    to_name = FLOWME_STATES[to_state]["name"]
    to_posture = FLOWME_STATES[to_state]["posture_adaptative"]
    
    return f"Pour passer de '{from_name}' vers '{to_name}' : {to_posture.lower()}"

def get_state_info(state_id: int) -> Dict[str, Any]:
    """
    Retourne les informations complètes d'un état
    
    Args:
        state_id: ID de l'état (1-64)
    
    Returns:
        Dictionnaire avec toutes les informations de l'état
    """
    if state_id not in FLOWME_STATES:
        state_id = 1
    
    state = FLOWME_STATES[state_id]
    famille_info = FAMILLE_SYMBOLIQUE.get(state["famille_symbolique"], {})
    
    return {
        "id": state_id,
        "name": state["name"],
        "famille_symbolique": state["famille_symbolique"],
        "fonction_famille": famille_info.get("fonction", ""),
        "tension_dominante": state["tension_dominante"],
        "mot_cle": state["mot_cle"],
        "declencheurs": state["declencheurs"],
        "posture_adaptative": state["posture_adaptative"],
        "conseil_flowme": state["conseil_flowme"],
        "etats_compatibles": state["etats_compatibles"],
        "etats_sequentiels": state["etats_sequentiels"],
        "energie_famille": famille_info.get("énergie", "balanced")
    }

def get_compatible_states(state_id: int) -> List[int]:
    """
    Retourne les états compatibles avec l'état donné
    
    Args:
        state_id: ID de l'état
    
    Returns:
        Liste des IDs d'états compatibles
    """
    if state_id not in FLOWME_STATES:
        return [1, 24, 32, 44, 64]  # États universels
    
    return FLOWME_STATES[state_id]["etats_compatibles"]

def analyze_message_flow(message: str, previous_states: List[int] = None) -> Dict[str, Any]:
    """
    Analyse complète d'un message selon l'architecture FlowMe
    
    Args:
        message: Message à analyser
        previous_states: Liste des états précédents (historique)
    
    Returns:
        Analyse complète avec état, transitions, et recommandations
    """
    # Détecter l'état principal
    context = {"etat_precedent": previous_states[-1] if previous_states else None}
    detected_state = detect_flowme_state(message, context)
    
    # Obtenir les informations de l'état
    state_info = get_state_info(detected_state)
    
    # Analyser les tendances si historique disponible
    tendance = "stable"
    if previous_states and len(previous_states) >= 3:
        recent_families = []
        for state_id in previous_states[-3:]:
            if state_id in FLOWME_STATES:
                recent_families.append(FLOWME_STATES[state_id]["famille_symbolique"])
        
        if len(set(recent_families)) == 1:
            tendance = "cyclique"
        elif "Montée & excès" in recent_families:
            tendance = "intensive"
        elif "Recul & germination" in recent_families:
            tendance = "contemplative"
        else:
            tendance = "exploratoire"
    
    # Générer conseil adapté
    advice = get_state_advice(detected_state, message, context)
    
    return {
        "detected_state": detected_state,
        "state_info": state_info,
        "advice": advice,
        "flow_tendency": tendance,
        "message_analysis": {
            "length": len(message.split()),
            "question_count": message.count("?"),
            "emotional_markers": _detect_emotional_markers(message),
            "urgency_level": _assess_urgency(message)
        },
        "recommendations": {
            "immediate_action": state_info["posture_adaptative"],
            "compatible_explorations": get_compatible_states(detected_state),
            "natural_progressions": state_info["etats_sequentiels"]
        }
    }

def _detect_emotional_markers(message: str) -> List[str]:
    """Détecte les marqueurs émotionnels dans le message"""
    markers = []
    message_lower = message.lower()
    
    emotional_patterns = {
        "joie": ["heureux", "content", "joie", "ravi", "enchanté"],
        "inquiétude": ["inquiet", "soucieux", "préoccupé", "angoissé"],
        "confusion": ["confus", "perdu", "désorienté", "mélangé"],
        "détermination": ["déterminé", "motivé", "résolu", "décidé"],
        "fatigue": ["fatigué", "épuisé", "las", "usé"],
        "curiosité": ["curieux", "intéressé", "intrigué"]
    }
    
    for emotion, words in emotional_patterns.items():
        if any(word in message_lower for word in words):
            markers.append(emotion)
    
    return markers

def _assess_urgency(message: str) -> str:
    """Évalue le niveau d'urgence du message"""
    message_lower = message.lower()
    
    high_urgency = ["urgent", "rapidement", "vite", "immédiatement", "maintenant", "!"]
    medium_urgency = ["bientôt", "prochainement", "assez vite"]
    
    if any(marker in message_lower for marker in high_urgency) or message.count("!") > 1:
        return "élevée"
    elif any(marker in message_lower for marker in medium_urgency):
        return "modérée"
    else:
        return "faible"

# Fonction de test et validation
def test_flowme_detection():
    """Teste le système de détection avec des exemples"""
    test_messages = [
        "Bonjour, j'aimerais commencer un nouveau projet",
        "Je me sens un peu perdu dans tout ça",
        "Pourquoi est-ce que ça ne fonctionne pas ?",
        "Je suis très stressé et j'ai besoin d'aide rapidement !",
        "Merci beaucoup, cela m'a vraiment aidé",
        "Je cherche à comprendre cette situation complexe",
        "Tout va bien, je suis en harmonie avec mon travail",
        "J'ai l'impression de tourner en rond"
    ]
    
    print("🧪 Test du système de détection FlowMe\n")
    
    for i, message in enumerate(test_messages, 1):
        detected = detect_flowme_state(message)
        state_info = get_state_info(detected)
        
        print(f"Test {i}: {message}")
        print(f"→ État détecté: {detected} - {state_info['name']}")
        print(f"→ Famille: {state_info['famille_symbolique']}")
        print(f"→ Mot-clé: {state_info['mot_cle']}")
        print()

if __name__ == "__main__":
    test_flowme_detection()
