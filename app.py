from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search_products(keyword: str):
    try:
        # Endpoint público de busca da Shopee Brasil
        url = f"https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword={keyword}&limit=10&newest=0&order=desc&page_type=search"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://shopee.com.br/"
        }

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        products = []
        items = data.get("items", [])
        
        for item in items:
            img = item.get("item_image", "")
            if img and not img.startswith("http"):
                img = f"https://cf.shopee.com.br/file/{img}"
            
            price = item.get("price_min_before_discount", item.get("price_min", 0)) / 100000
            
            products.append({
                "title": item.get("name", "Produto sem nome"),
                "price": f"{price:.2f}",
                "image": img,
                "sold": item.get("historical_sold", 0)
            })
            
        return {"products": products}
        
    except Exception as e:
        print(f"Erro na busca: {e}")
        return {"products": []}

@app.post("/generate")
async def generate_video(data: dict):
    return {
        "titulo": f"🔥 Achadinho: {data.get('keyword', 'Produto')}",
        "roteiro": "Roteiro gerado pela IA...",
        "tags": ["shopee", "viral"],
        "audio_base64": ""
    }
