from fastapi import FastAPI, UploadFile, File
import os
from openai import OpenAI
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@app.get("/")
def home():
    return {"status": "backend activo"}

@app.post("/run_campaign_creatives")
async def run_campaign_creatives(image: UploadFile = File(...)):
    
    prompts = [
        "Fondo beige premium minimalista",
        "Fondo gris cálido elegante",
        "Fondo piedra clara natural",
        "Fondo madera clara suave",
        "Fondo pastel suave publicitario",
        "Fondo crema luminoso",
        "Fondo degradado minimal",
        "Fondo estudio claro",
        "Fondo natural premium",
        "Fondo neutro elegante"
    ]

    return {
        "message": "10 prompts generados",
        "prompts": prompts
    }
