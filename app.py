from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import hashlib
import hmac
import time
import os

app = FastAPI()

# Libera acesso para seu site no Tiiny/Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pega suas chaves oficiais do Render
PARTNER_ID = os.getenv("SHOPEE_APP_ID")
PARTNER_KEY = os.getenv("SHOPEE_APP_KEY")

def generate_sign(path, params):
    """Cria a assinatura oficial exigida pela Shopee Open Platform"""
    if not PARTNER_KEY:
        return ""
    
    # Ordena os parâmetros alfabeticamente
    sorted_params = sorted(params.items())
    base_string = f"{PARTNER_ID}{path}"
    
    for key, value in sorted_params:
        base_string += f"{key}{value}"
        
    # Gera o hash HMAC-SHA256
    sign = hmac.new(
        PARTNER_KEY.encode('utf-8'),
        base_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return sign

@app.get("/search")
async def search_products(keyword: str):
    if not PARTNER_ID or not PARTNER_KEY:
        return {"products": [], "error": "Chaves da Shopee não configuradas no servidor"}

    # Endpoint oficial de busca de afiliados
    api_path = "/api/v2/item/search"
    base_url = f"https://partner.shopeemobile.com{api_path}"
    
    timestamp = int(time.time())
    
    # Parâmetros obrigatórios da API v2
    params = {
        "partner_id": int(PARTNER_ID),
        "timestamp": timestamp,
        "keyword": keyword,
        "limit": 10,
        "offset": 0
    }
    
    # Gera a assinatura oficial
    params["sign"] = generate_sign(api_path, params)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        products = []
        # A resposta oficial vem dentro de "response" -> "item_list"
        item_list = data.get("response", {}).get("item_list", [])
        
        for item in item_list:
            img = item.get("item_image", "")
            # A Shopee às vezes manda só o caminho da imagem
            if img and not img.startswith("http"):
                img = f"https://{img}"
            
            # Preço vem em micro-centavos (divide por 100000)
            price = float(item.get("item_price", 0)) / 100000
            
            products.append({
                "title": item.get("item_name", "Produto sem nome"),
                "price": f"{price:.2f}",
                "image": img,
                "sold": item.get("historical_sold", 0)
            })
            
        return {"products": products}
        
    except Exception as e:
        print(f"Erro na API Oficial Shopee: {e}")
        return {"products": [], "debug": str(e)}

@app.post("/generate")
async def generate_video(data: dict):
    return {"titulo": "Vídeo Viral", "roteiro": "Roteiro IA...", "audio_base64": ""}
