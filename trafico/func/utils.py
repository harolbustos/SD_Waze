import requests

def obtener_eventos(api_url):
    try:
        r = requests.get(f"{api_url}/eventos")
        r.raise_for_status()
        print(f"✅ Recibidos {len(r.json())} eventos totales.")
    except Exception as e:
        print(f"❌ Error en /eventos: {e}")

def obtener_eventos_por_tipo(api_url, tipo):
    try:
        r = requests.get(f"{api_url}/eventos?type={tipo}")
        r.raise_for_status()
        print(f"✅ {len(r.json())} eventos de tipo {tipo}.")
    except Exception as e:
        print(f"❌ Error en /eventos?type={tipo}: {e}")

def obtener_tipos_disponibles(api_url):
    try:
        r = requests.get(f"{api_url}/eventos/por-tipo")
        r.raise_for_status()
        return [x["_id"] for x in r.json()]
    except Exception:
        return []
