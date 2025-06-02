import datetime
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECCION_ORIGEN = os.getenv("COLLECCION_ORIGEN")
COLLECCION_DESTINO = os.getenv("COLLECCION_DESTINO")
EXPORT_PATH = os.getenv("EXPORT_PATH")

CAMPOS_REQUERIDOS = ["uuid", "type", "location", "pubMillis", "city"]

def conectar_mongo():
    cliente = pymongo.MongoClient(MONGO_URI)
    db = cliente[DB_NAME]
    return db[COLLECCION_ORIGEN], db[COLLECCION_DESTINO]

def evento_valido(evento):
    datos = evento.get("datos", {})
    return all(campo in datos for campo in CAMPOS_REQUERIDOS)

def limpiar_evento(evento):
    datos = evento["datos"]
    return {
        "wid": datos["uuid"],
        "evento": datos["type"],
        "descripcion": datos["subtype"],
        "lat": datos["location"]["y"],
        "lon": datos["location"]["x"],
        "comuna": evento["datos"]["city"],
        "timestamp": datos["pubMillis"],
        "fecha": datetime.datetime.fromtimestamp(datos["pubMillis"] / 1000).strftime("%Y-%m-%d %H:%M:%S")

    }

def procesar_eventos():
    col_origen, col_destino = conectar_mongo()
    vistos = set()
    filtrados = []

    print("🔄 Procesando eventos...")

    for evento in col_origen.find():
        if not evento_valido(evento):
            continue
        if evento["uuid"] in vistos:
            continue

        limpio = limpiar_evento(evento)
        filtrados.append(limpio)
        vistos.add(evento["uuid"])

    print(f"✅ Total válidos: {len(filtrados)}")

    # Guardar en MongoDB en la collecion 'eventos_filtados'
    col_destino.drop()
    col_destino.insert_many(filtrados)
    print("📦 Guardado en colección eventos_filtrados")

    # Exportar CSV
    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        f.write("wid,evento,descripcion,fecha,comuna,lat,lon,timestamp\n")
        for ev in filtrados:
            linea = f'{ev["wid"]},{ev["evento"]},{ev["descripcion"]},{ev["fecha"]},{ev["comuna"]},{ev["lat"]},{ev["lon"]},{ev["timestamp"]}\n'
            f.write(linea)

    print(f"📝 Exportado a archivo: {EXPORT_PATH}")

if __name__ == "__main__":
    procesar_eventos()