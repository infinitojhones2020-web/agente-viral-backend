from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Configuração CORS para permitir acesso do Netlify/Tiiny
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lê as chaves que você configurou no Render
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_APP_KEY = os.getenv("SHOPEE_APP_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/search")
async def search_products(keyword: str):
    if not SHOPEE_APP_ID or not SHOPEE_APP_KEY:
        return {"products": [], "error": "Credenciais da Shopee não configuradas no servidor"}

    # Endpoint de busca (Ajuste conforme a documentação oficial da Shopee Open Platform)
    # Nota: A API da Shopee geralmente exige assinatura e timestamp. 
    # Abaixo é um exemplo simplificado. Se der erro, precisaremos adicionar a lógica de assinatura HMAC.
    url = "https://partner.shopeemobile.com/api/v2/item/search" 
    
    headers = {
        "Content-Type": "application/json",
        # A Shopee pode exigir headers específicos de autorização dependendo da versão da API
    }
    
    params = {
        "partner_id": SHOPEE_APP_ID,
        "keyword": keyword,
        "limit": 10,
        # Outros parâmetros necessários pela API oficial
    }

    try:
        # Tenta buscar na API Oficial
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        products = []
        # Adaptação da resposta da Shopee para o formato do seu Frontend
        # ATENÇÃO: A estrutura exata depende da versão da API (v2 ou open_api)
        item_list = data.get("response", {}).get("item_list", []) 
        
        for item in item_list:
            products.append({
                "title": item.get("item_name", "Produto sem nome"),
                "price": float(item.get("item_price", 0)) / 100000, # Shopee costuma enviar em micro-centavos
                "image": f"https://{item.get('item_image', '')}",
                "sold": item.get("historical_sold", 0)
            })
                
        return {"products": products}
        
    except Exception as e:
        print(f"Erro na API Shopee: {e}")
        # Fallback: Retorna vazio em caso de erro para não quebrar o frontend
        return {"products": []}

@app.post("/generate")
async def generate_video(data: dict):
    # Lógica de geração de roteiro com Groq (mantenha sua lógica atual se já funcionar)
    return {
        "titulo": f"🔥 Achadinho: {data.get('keyword', 'Produto')}",
        "roteiro": "Roteiro gerado pela IA...",
        "tags": ["shopee", "viral"],
        "audio_base64": "" 
    }
