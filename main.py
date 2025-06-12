from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from flowme_states_detection_v03 import detect_flowme_state
from flowme_conflict_resolution import resolve_conflict

app = FastAPI()

# 🔧 Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pour développement ; restreindre pour prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Flowme backend operational."}

@app.post("/analyze")
async def analyze_text(request: Request):
    data = await request.json()
    text = data.get("text", "")
    state = detect_flowme_state(text)  # ✅ Fonction correcte
    return {"state": state}

@app.post("/resolve")
async def resolve_state_conflict(request: Request):
    data = await request.json()
    conflict = data.get("conflict", {})  # Gardé comme dans l'original
    resolved = resolve_conflict(conflict)
    return {"resolved_state": resolved}
