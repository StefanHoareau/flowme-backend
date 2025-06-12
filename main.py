from fastapi import FastAPI, Request
from flowme_states_detection_v03 import detect_flowme_state
from flowme_conflict_resolution import resolve_conflict

app = FastAPI()

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
