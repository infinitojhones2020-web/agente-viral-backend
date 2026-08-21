from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import hashlib
import hmac
import time
import os
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SHOPEE_PARTNER_ID = os.getenv("SHOPEE_APP_ID")      # Seu Partner ID
SHOPEE_PARTNER_KEY = os.getenv("SHOPEE_APP_KEY")    # Sua Partner Key

def generate_sign(url_path, params_dict):
    """Gera a assinatura HMAC-SHA256 exigida pela Shopee"""
    if not SHOPEE_PARTNER_KEY:
        return ""
    
    # Ordena os parâmetros e concatena
    sorted_params = sorted(params_dict.items())
    base_string = f"{SHOPEE_PARTNER_ID}{url_path}"
    for key, value in sorted_params:
        base_string += f"{key}{value}"
    
    # Gera o hash
    sign = hmac.new(
        SHOPEE_PARTNER_KEY.encode('utf-8'),
        base_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return sign

@app.get("/search")
async def search_products(keyword: str):
    if not SHOPEE_PARTNER_ID or not SHOPEE_PARTNER_KEY:
        return {"products": [], "error": "Credenciais não configuradas"}

    # Endpoint oficial da Shopee Open Platform v2
    api_path = "/api/v2/item/search"
    base_url = f"https://partner.shopeemobile.com{api_path}"
    
    timestamp = int(time.time())
    
    params = {
        "partner_id": int(SHOPEE_PARTNER_ID),
        "timestamp": timestamp,
        "keyword": keyword,
        "limit": 10,
        "offset": 0
    }
    
    # Gera a assinatura
    sign = generate_sign(api_path, params)
    params["sign"] = sign
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        products = []
        # A estrutura de resposta da Shopee v2
        item_list = data.get("response", {}).get("item_list", [])
        
        for item in item_list:
            img_url = item.get("item_image", "")
            if img_url and not img_url.startswith("http"):
                img_url = f"https://{img_url}"
                
            products.append({
                "title": item.get("item_name", "Produto sem nome"),
                "price": float(item.get("item_price", 0)) / 100000,  # Shopee usa micro-centavos
                "image": img_url,
                "sold": item.get("historical_sold", 0)
            })
            
        return {"products": products}
        
    except Exception as e:
        print(f"Erro Shopee: {e}")
        return {"products": []}

@app.post("/generate")
async def generate_video(data: dict):
    return {
        "titulo": f"🔥 Achadinho: {data.get('keyword', 'Produto')}",
        "roteiro": "Roteiro gerado pela IA...",
        "tags": ["shopee", "viral"],
        "audio_base64": ""
    }
