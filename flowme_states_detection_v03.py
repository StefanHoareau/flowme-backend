def detect_flowme_state(text):
    # Détection simple d'exemple
    if "fatigue" in text.lower():
        return "Fatigue"
    elif "curiosité" in text.lower():
        return "Curiosité"
    return "Inconnu"
