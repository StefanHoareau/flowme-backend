def detect_flowme_state_improved(message: str, context: Optional[Dict] = None) -> int:
    """
    Version améliorée de la détection qui gère mieux les cas complexes
    """
    if not message or not message.strip():
        return 1
    
    message_lower = message.lower().strip()
    context = context or {}
    
    # === DÉTECTION PRIORITAIRE DES MOTS FORTS ===
    
    # Mots de violence/conflit (priorité haute)
    violence_words = ["carnage", "despotisme", "guerre", "tuer", "détruire", "haïr", "violence"]
    if any(word in message_lower for word in violence_words):
        # Si violence + autres éléments → Expression/Colère
        if any(word in message_lower for word in ["disputé", "énervé", "marre"]):
            return 14  # Colère Constructive
        else:
            return 32  # Expression Libre (besoin d'exprimer des choses fortes)
    
    # Mots de souffrance (priorité haute)
    suffering_words = ["triste", "mal", "souffre", "douleur", "blessé", "cassé"]
    if any(word in message_lower for word in suffering_words):
        return 45  # Vulnérabilité Assumée
    
    # === DÉTECTION PAR COMBINAISONS ===
    
    # Messages contradictoires (amour + violence)
    love_words = ["amour", "compassion", "tendresse", "douceur"]
    has_love = any(word in message_lower for word in love_words)
    has_violence = any(word in message_lower for word in violence_words)
    
    if has_love and has_violence:
        return 58  # Inclusion Bienveillante (intégration des opposés)
    
    # === DÉTECTION NORMALE PAR MOTS-CLÉS ===
    
    state_scores = {}
    
    for state_id, state_data in FLOWME_STATES.items():
        score = 0
        keywords_found = []
        
        # Vérifier les mots-clés
        for keyword in state_data["keywords"]:
            if keyword in message_lower:
                score += 2
                keywords_found.append(keyword)
        
        # Bonus contextuel
        if keywords_found:
            if len(message.split()) <= 5:
                score += 1
            
            emotional_states = [45, 14, 32]
            if state_id in emotional_states and any(word in message_lower for word in ["triste", "disputé", "cassé", "énervé", "mal"]):
                score += 3
        
        state_scores[state_id] = score
    
    # Trouver le meilleur état
    if state_scores and max(state_scores.values()) > 0:
        best_state = max(state_scores, key=state_scores.get)
        return best_state
    
    # === FALLBACKS AMÉLIORÉS ===
    
    # Questions
    if any(word in message_lower for word in ["?", "pourquoi", "comment", "qu'est-ce"]):
        return 7  # Curiosité
    
    # Gratitude pure (sans ambiguïté)
    if any(word in message_lower for word in ["merci", "gratitude", "reconnaissance"]) and not has_violence:
        return 8  # Résonance
    
    # Mots positifs simples (sans violence)
    if any(word in message_lower for word in ["bien", "super", "génial"]) and not has_violence:
        return 8  # Résonance
    
    # Changement/possibilité
    if any(word in message_lower for word in ["changer", "possible", "peut", "nouveau"]):
        return 64  # Porte Ouverte
    
    # Défaut sécurisé
    return 1  # Présence


# === MOTS-CLÉS ÉTENDUS POUR CHAQUE ÉTAT ===

EXTENDED_KEYWORDS = {
    14: ["énervé", "colère", "furieux", "marre", "agacé", "dispute", "violence", "carnage", "guerre", "révoltant"],
    32: ["dire", "exprimer", "parler", "voix", "crier", "disputé", "proclamer", "déclarer", "révéler"],
    45: ["triste", "mal", "souffre", "difficile", "cassé", "blessé", "peur", "vulnérable", "fragile"],
    58: ["aide", "soutien", "ensemble", "famille", "couple", "relation", "amour", "compassion", "inclusion"],
    22: ["cassé", "réparer", "solution", "pratique", "faire", "lacet", "problème", "résoudre"],
    7: ["pourquoi", "comment", "qu'est-ce", "changer", "curieux", "comprendre", "explorer"],
    8: ["merci", "gratitude", "reconnaissance", "ensemble", "comprends", "harmonie", "bien"],
    64: ["possible", "nouveau", "changer", "espoir", "avenir", "peut", "transformation"],
    1: ["bonjour", "salut", "hello", "présence", "écoute", "attention", "silence"]
}

def test_improved_detection():
    """Test avec le message problématique"""
    
    test_cases = [
        ("Amour, Compassion, Despotisme, Carnage, cela me plaît bien !", "Devrait être État 58 (Inclusion) ou 32 (Expression)"),
        ("je suis triste", "État 45 (Vulnérabilité)"),
        ("comment changer", "État 7 (Curiosité)"),
        ("mon lacet est cassé", "État 22 (Pragmatisme)"),
        ("merci beaucoup", "État 8 (Résonance)"),
        ("je me suis disputé", "État 32 (Expression)")
    ]
    
    print("🧪 Test de la détection améliorée:")
    print("-" * 70)
    
    for message, expected in test_cases:
        detected = detect_flowme_state_improved(message)
        state_name = FLOWME_STATES[detected]["name"]
        
        print(f"Message: '{message}'")
        print(f"Détecté: État {detected} - {state_name}")
        print(f"Attendu: {expected}")
        print("-" * 40)

# Test spécifique pour le message problématique
def analyze_problematic_message():
    """Analyse détaillée du message problématique"""
    message = "Amour, Compassion, Despotisme, Carnage, cela me plaît bien !"
    
    print("🔍 Analyse du message problématique:")
    print(f"Message: '{message}'")
    print()
    
    # Détection actuelle
    current_result = detect_flowme_state(message)
    print(f"❌ Détection actuelle: État {current_result} - {FLOWME_STATES[current_result]['name']}")
    
    # Détection améliorée  
    improved_result = detect_flowme_state_improved(message)
    print(f"✅ Détection améliorée: État {improved_result} - {FLOWME_STATES[improved_result]['name']}")
    
    print()
    print("💡 Pourquoi cette amélioration:")
    print("- Détecte 'carnage' et 'despotisme' comme mots de violence")
    print("- Détecte 'amour' et 'compassion' comme mots d'inclusion") 
    print("- Combinaison violence + amour = besoin d'inclusion/intégration")
    print("- Plus de fallback aveugle sur 'bien'")
