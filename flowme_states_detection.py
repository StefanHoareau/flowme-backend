# Amélioration de la détection FlowMe avec analyse sémantique

import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class AdvancedFlowMeDetection:
    """Détection FlowMe avec analyse sémantique et contextuelle avancée"""
    
    def __init__(self):
        self.emotional_patterns = {
            "tristesse": {
                "primary": ["triste", "pleurer", "larmes", "chagrin", "déprimé"],
                "context": ["mort", "perte", "séparation", "échec", "solitude"],
                "intensity": {"léger": 1, "modéré": 2, "intense": 3}
            },
            "colère": {
                "primary": ["énervé", "furieux", "colère", "rage", "irrité"],
                "context": ["injustice", "conflit", "frustration", "dispute"],
                "intensity": {"agacement": 1, "colère": 2, "rage": 3}
            },
            "curiosité": {
                "primary": ["pourquoi", "comment", "qu'est-ce", "comprendre"],
                "context": ["apprendre", "découvrir", "explorer", "questionner"],
                "intensity": {"intérêt": 1, "curiosité": 2, "passion": 3}
            }
        }
        
        self.contextual_modifiers = {
            "temporel": {
                "passé": ["était", "avait", "hier", "avant", "autrefois"],
                "présent": ["est", "maintenant", "actuellement", "en ce moment"],
                "futur": ["sera", "demain", "bientôt", "espère", "vais"]
            },
            "relationnel": {
                "intime": ["ami", "famille", "parent", "conjoint", "enfant"],
                "professionnel": ["travail", "collègue", "patron", "bureau"],
                "social": ["société", "monde", "gens", "autres", "groupe"]
            }
        }
    
    def analyze_semantic_depth(self, message: str) -> Dict:
        """Analyse sémantique approfondie du message"""
        
        # Analyse des patterns émotionnels
        emotional_analysis = self._detect_emotional_patterns(message)
        
        # Analyse du contexte temporel
        temporal_context = self._analyze_temporal_context(message)
        
        # Analyse relationnelle
        relational_context = self._analyze_relational_context(message)
        
        # Analyse de l'intensité
        intensity_level = self._calculate_intensity(message, emotional_analysis)
        
        return {
            "emotional_patterns": emotional_analysis,
            "temporal_context": temporal_context,
            "relational_context": relational_context,
            "intensity_level": intensity_level,
            "semantic_score": self._calculate_semantic_score(
                emotional_analysis, temporal_context, relational_context, intensity_level
            )
        }
    
    def _detect_emotional_patterns(self, message: str) -> Dict:
        """Détecte les patterns émotionnels dans le message"""
        message_lower = message.lower()
        detected_emotions = {}
        
        for emotion, patterns in self.emotional_patterns.items():
            score = 0
            matched_words = []
            
            # Vérifier les mots primaires
            for word in patterns["primary"]:
                if word in message_lower:
                    score += 2
                    matched_words.append(word)
            
            # Vérifier le contexte
            for word in patterns["context"]:
                if word in message_lower:
                    score += 1
                    matched_words.append(f"context:{word}")
            
            if score > 0:
                detected_emotions[emotion] = {
                    "score": score,
                    "matched_words": matched_words
                }
        
        return detected_emotions
    
    def _analyze_temporal_context(self, message: str) -> str:
        """Analyse le contexte temporel"""
        message_lower = message.lower()
        
        temporal_scores = {}
        for time_context, words in self.contextual_modifiers["temporel"].items():
            score = sum(1 for word in words if word in message_lower)
            if score > 0:
                temporal_scores[time_context] = score
        
        return max(temporal_scores, key=temporal_scores.get) if temporal_scores else "présent"
    
    def _analyze_relational_context(self, message: str) -> str:
        """Analyse le contexte relationnel"""
        message_lower = message.lower()
        
        relational_scores = {}
        for rel_context, words in self.contextual_modifiers["relationnel"].items():
            score = sum(1 for word in words if word in message_lower)
            if score > 0:
                relational_scores[rel_context] = score
        
        return max(relational_scores, key=relational_scores.get) if relational_scores else "personnel"
    
    def _calculate_intensity(self, message: str, emotional_analysis: Dict) -> int:
        """Calcule l'intensité émotionnelle"""
        base_intensity = 1
        
        # Intensité basée sur la ponctuation
        if "!" in message:
            base_intensity += 1
        if "!!!" in message:
            base_intensity += 2
        
        # Intensité basée sur les mots émotionnels trouvés
        total_emotional_score = sum(data["score"] for data in emotional_analysis.values())
        if total_emotional_score > 3:
            base_intensity += 1
        
        # Intensité basée sur la longueur et répétition
        words = message.split()
        if len(words) > 20:  # Message long = intensité potentielle
            base_intensity += 1
        
        return min(base_intensity, 5)  # Max 5
    
    def _calculate_semantic_score(self, emotional: Dict, temporal: str, 
                                relational: str, intensity: int) -> float:
        """Calcule un score sémantique global"""
        base_score = sum(data["score"] for data in emotional.values())
        
        # Bonus pour contexte temporel spécifique
        temporal_bonus = {"passé": 0.5, "futur": 0.3, "présent": 0.2}
        base_score += temporal_bonus.get(temporal, 0)
        
        # Bonus pour contexte relationnel
        relational_bonus = {"intime": 0.8, "professionnel": 0.5, "social": 0.3}
        base_score += relational_bonus.get(relational, 0)
        
        # Multiplicateur d'intensité
        final_score = base_score * (1 + intensity * 0.2)
        
        return round(final_score, 2)

# Extension pour FlowMe avec détection avancée
def enhanced_flowme_detection(message: str, previous_states: List[int] = None) -> Dict:
    """Détection FlowMe améliorée avec analyse sémantique"""
    
    detector = AdvancedFlowMeDetection()
    semantic_analysis = detector.analyze_semantic_depth(message)
    
    # Votre détection existante
    basic_state = detect_flowme_state(message)
    
    # Modulation basée sur l'analyse sémantique
    modulated_state = _modulate_state_with_semantics(
        basic_state, semantic_analysis, previous_states
    )
    
    return {
        "detected_state": modulated_state,
        "semantic_analysis": semantic_analysis,
        "confidence_score": semantic_analysis["semantic_score"],
        "reasoning": _generate_detection_reasoning(semantic_analysis, modulated_state)
    }

def _modulate_state_with_semantics(basic_state: int, semantic: Dict, 
                                 history: List[int] = None) -> int:
    """Module l'état de base avec l'analyse sémantique"""
    
    emotions = semantic["emotional_patterns"]
    intensity = semantic["intensity_level"]
    temporal = semantic["temporal_context"]
    
    # Si forte tristesse + haute intensité → État 45 (Vulnérabilité)
    if "tristesse" in emotions and emotions["tristesse"]["score"] >= 3 and intensity >= 3:
        return 45
    
    # Si curiosité + contexte futur → État 64 (Porte Ouverte)  
    elif "curiosité" in emotions and temporal == "futur":
        return 64
    
    # Si colère + contexte relationnel → État 14 (Colère Constructive)
    elif "colère" in emotions and semantic["relational_context"] == "intime":
        return 14
    
    # Sinon, utiliser l'état de base mais avec confiance ajustée
    return basic_state

def _generate_detection_reasoning(semantic: Dict, final_state: int) -> str:
    """Génère une explication de la détection"""
    emotions = list(semantic["emotional_patterns"].keys())
    intensity = semantic["intensity_level"]
    temporal = semantic["temporal_context"]
    
    if emotions:
        emotion_text = f"Émotions détectées: {', '.join(emotions)}"
    else:
        emotion_text = "Pas d'émotion forte détectée"
    
    return f"{emotion_text}. Intensité: {intensity}/5. Contexte: {temporal}. → État {final_state}"
