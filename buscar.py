import googlemaps
import pandas as pd
import time

# ==========================================
# CONFIGURAÇÕES
# ==========================================
API_KEY = 'AIzaSyCjvr34AjPzNZx8tu9GZmX68cBUhg80B7M'  # <--- Sua chave já está aqui

ENDERECO = "R. Augusto de Almeida Batista, 1942, Jardim Vazame, Embu das Artes - SP"
RAIO_METROS = 5000

PALAVRAS_CHAVE = [
    "Marcenaria", "sob medida", "moveis", "móveis", 
    "MDF", "planejados", "planejado", "montador"
]
# ==========================================

def buscar_mymaps():
    print(f"📍 Base: {ENDERECO}")
    print(f"📡 Raio: {RAIO_METROS}m | 🗺️ Preparando para Google My Maps...")

    try:
        gmaps = googlemaps.Client(key=API_KEY)
        geocode_result = gmaps.geocode(ENDERECO)
        if not geocode_result:
            print("❌ Endereço base não encontrado. Verifique se a API Geocoding está ativada.")
            return
        location = geocode_result[0]['geometry']['location']
        lat_lng = (location['lat'], location['lng'])
    except Exception as e:
        print(f"❌ Erro de conexão ou chave inválida: {e}")
        return

    resultados = []
    ids_processados = set()

    for termo in PALAVRAS_CHAVE:
        print(f"🔎 Buscando: '{termo}'...")
        
        try:
            places_result = gmaps.places_nearby(location=lat_lng, radius=RAIO_METROS, keyword=termo)
        except Exception as e:
            print(f"   Erro na busca (verifique se a Places API está ativada): {e}")
            continue
        
        while True:
            for place in places_result.get('results', []):
                place_id = place['place_id']
                
                if place_id in ids_processados:
                    continue
                ids_processados.add(place_id)

                # ADICIONADO: 'geometry' para pegar Latitude e Longitude
                try:
                    detalhes = gmaps.place(
                        place_id, 
                        fields=['name', 'formatted_address', 'formatted_phone_number', 'geometry']
                    )
                    dados = detalhes.get('result', {})
                    
                    # Extraindo coordenadas
                    geo = dados.get('geometry', {}).get('location', {})
                    lat = geo.get('lat', 0)
                    lng = geo.get('lng', 0)

                    item = {
                        'Nome': dados.get('name'),
                        'Endereco': dados.get('formatted_address'),
                        'Telefone': dados.get('formatted_phone_number', 'Não informado'),
                        'Latitude': lat,    # <--- Essencial para My Maps
                        'Longitude': lng,   # <--- Essencial para My Maps
                        'Termo': termo
                    }
                    resultados.append(item)
                    print(f"   📍 {item['Nome']}")

                except Exception as e:
                    print(f"   Erro detalhes: {e}")

            token = places_result.get('next_page_token')
            if not token:
                break
            time.sleep(2) # Pausa obrigatória do Google
            try:
                places_result = gmaps.places_nearby(location=lat_lng, radius=RAIO_METROS, keyword=termo, page_token=token)
            except:
                break

    if resultados:
        # Salva em CSV padrão (vírgula) que o Google My Maps aceita melhor
        df = pd.DataFrame(resultados)
        arquivo = 'marcenarias_para_mapa.csv'
        df.to_csv(arquivo, index=False, encoding='utf-8')
        
        print(f"\n✅ SUCESSO! {len(resultados)} locais salvos.")
        print(f"📂 Arquivo gerado: {arquivo}")
        print("➡️  Agora importe este arquivo no Google My Maps (google.com/mymaps).")
    else:
        print("\n❌ Nada encontrado.")

if __name__ == "__main__":
    buscar_mymaps()