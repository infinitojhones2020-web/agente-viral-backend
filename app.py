import os, json, base64, httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import edge_tts

app = FastAPI()
GROQ_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

class SearchReq(BaseModel):
    keyword: str

@app.get("/search")
async def search(keyword: str):
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword={keyword}&limit=6"
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            data = resp.json()
            products = []
            for item in data.get('items', [])[:6]:
                info = item.get('item_basic', {})
                img_id = info.get('images', [{}])[0].get('image_id') if info.get('images') else ''
                products.append({
                    "id": info.get('itemid'),
                    "title": info.get('name'),
                    "price": info.get('price') / 100000,
                    "image": f"https://cf.shopee.com.br/file/{img_id}",
                    "sold": info.get('historical_sold', 0)
                })
            return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_video_assets(req: SearchReq):
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq Key faltando")

    prompt = f"""Crie um roteiro viral de 15s para TikTok/Shopee sobre: '{req.keyword}'.
    Tom: Brasileiro, natural, entusiasmado. 
    Retorne APENAS JSON: {{"titulo": "...", "tags": ["#tag"], "roteiro": "..."}}"""
    
    chat = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-70b-versatile",
        response_format={"type": "json_object"}
    )
    assets = json.loads(chat.choices[0].message.content)

    tts = edge_tts.Communicate(assets['roteiro'], "pt-BR-FranciscaNeural")
    audio_path = "/tmp/audio.mp3"
    await tts.save(audio_path)
    
    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

    return {**assets, "audio_base64": audio_b64}
