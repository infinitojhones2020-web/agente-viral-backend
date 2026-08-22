from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import hashlib
import hmac
import time
import os

app = FastAPI()

# Configuração de CORS para permitir acesso do seu site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega as chaves do Render
PARTNER_ID = os.getenv("SHOPEE_APP_ID")
PARTNER_KEY = os.getenv("SHOPEE_APP_KEY")

def generate_sign(path, params):
    """Função oficial de assinatura da Shopee"""
    if not PARTNER_KEY:
        return ""
    
    # Ordena os parâmetros
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

@app.get("/")
async def root():
    return {"status": "Servidor Online - Agente Viral"}

@app.get("/search")
async def search_products(keyword: str):
    if not PARTNER_ID or not PARTNER_KEY:
        return {"error": "Chaves da Shopee não encontradas no servidor"}

    api_path = "/api/v2/item/search"
    base_url = f"https://partner.shopeemobile.com{api_path}"
    
    timestamp = int(time.time())
    
    params = {
        "partner_id": int(PARTNER_ID),
        "timestamp": timestamp,
        "keyword": keyword,
        "limit": 10,
        "offset": 0
    }
    
    # Gera a assinatura
    params["sign"] = generate_sign(api_path, params)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        # MODO DEBUG: Retorna tudo para vermos o erro da Shopee
        return {
            "shopee_raw_response": data,
            "params_used": params,
            "partner_id_check": PARTNER_ID
        }
        
    except Exception as e:
        return {"error_connection": str(e)}

@app.post("/generate")
async def generate_video(data: dict):
    return {"titulo": "Vídeo Viral", "roteiro": "Roteiro IA..."}
