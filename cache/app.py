import os
import requests
from flask import Flask, jsonify, request
from sistema_cache.cache import SistemaCache
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

# Configuracion
API_BACKEND = os.getenv("API_BACKEND", "http://localhost:8080")
CACHE_SIZE = int(os.getenv("CACHE_SIZE"))
CACHE_POLICY = os.getenv("CACHE_POLICY")
PORT = int(os.getenv("PORT"))
HOST = os.getenv("HOST")

cache = SistemaCache(max_size=CACHE_SIZE, policy=CACHE_POLICY)

@app.route('/eventos')
def eventos():
    key = request.full_path
    data = cache.get(key)

    if data:
        print(f"⚡ [CACHÉ] HIT → {key}")
        return jsonify(data)

    print(f"🌐 [API] MISS → {key}")
    try:
        response = requests.get(f"{API_BACKEND}/eventos", params=request.args)
        if response.status_code == 200:
            data = response.json()
            cache.put(key, data)
            print(f"💾 [CACHÉ] GUARDADO → {key}")
            return jsonify(data)
        else:
            print(f"❌ [API ERROR] Código {response.status_code}")
            return jsonify({"error": f"API error: {response.status_code}"}), 500
    except Exception as e:
        print(f"❌ [ERROR] Al contactar API: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/eventos/por-tipo')
def eventos_por_tipo():
    print("📊 [AGRUPACIÓN] → /eventos/por-tipo")
    try:
        response = requests.get(f"{API_BACKEND}/eventos/por-tipo")
        return jsonify(response.json())
    except Exception as e:
        print(f"❌ [ERROR] Al obtener tipos: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/cache/metricas')
def metrics():
    print("[MÉTRICAS] → /cache/metricas")
    return jsonify(cache.metrics())


@app.get('/')
def index():
    return 'Hello, World!'

if __name__ == "__main__":
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    # print(f"🚀 Cache escuchando en http://{HOST}:{PORT}")
    print(f"🔁 Política de caché: {CACHE_POLICY}")
    print(f"📦 Tamaño máximo: {CACHE_SIZE}")
    print(f" Conexion al backend en  {API_BACKEND}")
    app.run(port=PORT, host=HOST)
