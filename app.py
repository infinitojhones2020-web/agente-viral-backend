@app.get("/search")
async def search_products(keyword: str):
    if not PARTNER_ID or not PARTNER_KEY:
        return {"error": "Chaves não configuradas"}

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
    
    params["sign"] = generate_sign(api_path, params)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        # Retorna TUDO o que a Shopee respondeu para debug
        return {
            "status_code": response.status_code,
            "shopee_response": data,
            "params_sent": params,
            "sign_generated": params["sign"]
        }
        
    except Exception as e:
        return {"error": str(e)}
