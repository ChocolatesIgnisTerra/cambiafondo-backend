from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
import base64
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()

@app.get("/")
def home():
    return {"status": "backend activo"}

@app.post("/run_campaign_creatives")
async def run_campaign_creatives(image: UploadFile = File(...)):
    image_bytes = await image.read()

    image_base64_analysis = base64.b64encode(image_bytes).decode("utf-8")
    mime_type = image.content_type or "image/jpeg"

    analysis = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_base64_analysis}"}
                    },
                    {
                        "type": "text",
                        "text": """Eres un director creativo de publicidad gourmet de lujo.
Analiza este producto y responde en este formato exacto:

PRODUCTO: [describe brevemente el producto]
OCASION: [detecta si el producto es alusivo a alguna ocasión especial: Pascua, Navidad, Día de la Madre, Día del Padre, Halloween, San Valentín, etc. Si no hay ocasión específica, escribe "everyday premium"]
FONDOS:
1
