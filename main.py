from fastapi import FastAPI, UploadFile, File
import os
from openai import OpenAI
import base64
from io import BytesIO

app = FastAPI()
client = OpenAI()

@app.get("/")
def home():
    return {"status": "backend activo"}

@app.post("/run_campaign_creatives")
async def run_campaign_creatives(image: UploadFile = File(...)):
    image_bytes = await image.read()

    prompt_system = """
Eres un experto en marketing visual y publicidad digital.
Analiza el producto de la imagen subida y genera 10 prompts de fondos publicitarios
para usar en generación de imágenes de marketing.
Los prompts deben ser cortos, claros y enfocados en fondos publicitarios como:
- fondo premium minimalista
- fondo piedra natural
- fondo madera suave
- fondo pastel publicitario
- fondo estudio limpio
- fondo elegante para ecommerce
- fondo vertical para historia de Instagram
- fondo para anuncio de Meta Ads
- fondo natural premium
- fondo neutro elegante
Devuelve solo una lista de 10 prompts.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": "Genera 10 prompts de fondos publicitarios para este producto."}
        ],
        temperature=0.7
    )

    text = response.choices[0].message.content
    prompts = [p.strip("- ").strip() for p in text.split("\n") if p.strip()]

    image_prompt = prompts[0]
    image_response = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024"
    )
    image_base64 = image_response.data[0].b64_json

    return {
        "message": "prompts e imagen generados",
        "prompts": prompts,
        "image_base64": image_base64
    }
