<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agente Viral Shopee - Produtos Reais</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; padding: 20px; max-width: 900px; margin: 0 auto; }
        h1 { text-align: center; color: #ee4d2d; }
        .search-box { display: flex; gap: 10px; margin-bottom: 30px; }
        input { flex: 1; padding: 12px; border-radius: 8px; border: none; font-size: 16px; }
        button { background: #ee4d2d; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        button:hover { background: #d03e1f; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
        .card { background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); }
        .card img { width: 100%; height: 180px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; background: #334155; }
        .price { color: #4ade80; font-weight: bold; font-size: 18px; margin-top: 5px; }
        .sold { color: #94a3b8; font-size: 12px; }
        .loading { text-align: center; color: #94a3b8; margin: 40px; font-size: 18px; }
        .error { text-align: center; color: #f87171; margin: 20px; }
    </style>
</head>
<body>
    <h1>🔥 Agente Viral Shopee (Direto)</h1>
    <div class="search-box">
        <input type="text" id="keyword" placeholder="Ex: Fone Bluetooth, Lip Tint..." value="fone bluetooth">
        <button onclick="buscarProdutos()">Buscar Tendências</button>
    </div>
    <div id="status" class="loading"></div>
    <div id="products" class="grid"></div>

    <script>
        async function buscarProdutos() {
            const keyword = document.getElementById('keyword').value;
            const status = document.getElementById('status');
            const grid = document.getElementById('products');
            
            if (!keyword) return;
            
            status.innerText = '🔍 Buscando produtos reais na Shopee...';
            status.style.display = 'block';
            grid.innerHTML = '';

            try {
                // Usa um proxy CORS público para acessar a API da Shopee direto do navegador
                const shopeeUrl = `https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword=${encodeURIComponent(keyword)}&limit=12&newest=0`;
                const proxyUrl = `https://api.allorigins.win/raw?url=${encodeURIComponent(shopeeUrl)}`;
                
                const response = await fetch(proxyUrl);
                const data = await response.json();
                
                const items = data?.items || [];
                
                if (items.length === 0) {
                    status.innerText = 'Nenhum produto encontrado. Tente outro termo.';
                    return;
                }

                status.style.display = 'none';
                
                grid.innerHTML = items.map(item => {
                    const price = (item.price_min_before_discount || item.price_min || 0) / 100000;
                    const image = item.item_image 
                        ? `https://cf.shopee.com.br/file/${item.item_image}` 
                        : 'https://via.placeholder.com/300x200?text=Sem+Imagem';
                    
                    return `
                        <div class="card">
                            <img src="${image}" alt="${item.name}" loading="lazy" onerror="this.src='https://via.placeholder.com/300x200?text=Erro+Imagem'">
                            <h3 style="font-size:14px; margin:0 0 5px 0; line-height:1.4">${item.name}</h3>
                            <div class="price">R$ ${price.toFixed(2).replace('.', ',')}</div>
                            <div class="sold">${item.historical_sold || 0} vendidos</div>
                            <button style="width:100%; margin-top:10px; background:#8b5cf6;" onclick="alert('Link de afiliado em breve!')">🎬 Gerar Vídeo Viral</button>
                        </div>
                    `;
                }).join('');
                
            } catch (e) {
                console.error(e);
                status.innerText = '⚠️ Erro ao buscar. A Shopee pode estar bloqueando. Tente novamente em 1 minuto.';
                status.className = 'error';
            }
        }

        // Busca automática ao carregar
        window.onload = () => buscarProdutos();
    </script>
</body>
</html>
