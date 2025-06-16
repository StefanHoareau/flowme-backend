from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

from flowme_states_detection import detect_state

app = FastAPI()

# CORS pour interface front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restreindre plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle d'entrée
class TextInput(BaseModel):
    text: str

# Fonction : appeler Mistral
def ask_mistral(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "top_p": 0.95
    }
    r = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
    return r.json()["choices"][0]["message"]["content"]

# Fonction : logger vers NocoDB
def log_to_nocodb(text: str, state: str, mistral_reply: str = ""):
    headers = {
        "Content-Type": "application/json",
        "xc-token": os.environ['NOCODB_API_KEY']
    }
    data = {
        "texte": text,
        "etat": state,
        "reponse_mistral": mistral_reply
    }
    url = f"{os.environ['NOCODB_URL']}/api/v1/db/data/v1/Flowme_States"
    requests.post(url, headers=headers, json=data)

# Endpoint principal
@app.post("/analyze")
async def analyze(input: TextInput):
    user_text = input.text
    detected_state = detect_state(user_text)
    
    # Préparer prompt pour Mistral
    prompt = f"L'utilisateur a exprimé : « {user_text} ». Réponds de façon bienveillante, concise et contextuelle en lien avec l’état émotionnel détecté : {detected_state}."

    # Appel à Mistral
    try:
        mistral_response = ask_mistral(prompt)
    except Exception as e:
        mistral_response = "(erreur de génération IA)"

    # Logger dans NocoDB
    try:
        log_to_nocodb(user_text, detected_state, mistral_response)
    except Exception as e:
        print("Erreur de logging NocoDB :", e)

    return {
        "state": detected_state,
        "response": mistral_response
    }
