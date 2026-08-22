from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Libera acesso para qualquer site (Netlify/Tiiny)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Servidor Agente Viral Online"}

@app.get("/search")
async def search_products(keyword: str):
    try:
        # Busca direta na API pública da Shopee Brasil
        url = f"https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword={keyword}&limit=6&newest=0"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://shopee.com.br/"
        }

        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        products = []
        for item in data.get("items", []):
            img = item.get("item_image", "")
            if img and not img.startswith("http"):
                img = f"https://cf.shopee.com.br/file/{img}"
            
            price = item.get("price_min_before_discount", item.get("price_min", 0)) / 100000
            
            products.append({
                "title": item.get("name", "Produto"),
                "price": f"{price:.2f}",
                "image": img,
                "sold": item.get("historical_sold", 0)
            })
            
        return {"products": products}
        
    except Exception as e:
        # Fallback seguro se a Shopee bloquear
        return {"products": [
            {"title": f"Achadinho: {keyword}", "price": "29.90", "image": "https://via.placeholder.com/300x200?text=Shopee+Viral", "sold": 1000}
        ]}

@app.post("/generate")
async def generate_video(data: dict):
    return {"titulo": "Vídeo Viral", "roteiro": "Roteiro IA...", "audio_base64": ""}
