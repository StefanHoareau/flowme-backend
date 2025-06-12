from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fonctions intégrées directement dans main.py
def detect_flowme_state(text):
    # Détection simple d'exemple
    if "fatigue" in text.lower():
        return "Fatigue"
    elif "curiosité" in text.lower():
        return "Curiosité"
    return "Inconnu"

def resolve_conflict(conflict):
    # Résolution fictive pour débuter
    return {"resolved": True, "details": "Conflit traité avec logique simplifiée."}

@app.get("/")
def read_root():
    return {"message": "Flowme backend operational."}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    text = data.get("text", "")
    detected_state = detect_flowme_state(text)
    return {"state": detected_state}

@app.post("/resolve")
async def resolve(request: Request):
    data = await request.json()
    conflict = data.get("conflict", {})
    resolution = resolve_conflict(conflict)
    return {"resolution": resolution}
