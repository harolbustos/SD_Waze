import csv
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELASTIC_URL = os.getenv("ELASTIC_URL")
HEADERS = {"Content-Type": "application/json"}


def convertir_valor(valor, tipo):
    try:
        if tipo == "int":
            return int(valor)
        elif tipo == "float":
            return float(valor)
        else:
            return valor
    except ValueError:
        return None


def cargar_csv_a_elasticsearch(ruta_csv, indice, campos, tipos):
    bulk_data = ""
    with open(ruta_csv, newline='', encoding='utf-8') as f:
        lector = csv.reader(f)
        for fila in lector:
            if len(fila) != len(campos):
                print(f"Fila con columnas inconsistentes: {fila}")
                continue

            fila_convertida = []
            for i, valor in enumerate(fila):
                valor_convertido = convertir_valor(valor.strip(), tipos[i])
                fila_convertida.append(valor_convertido)

            doc = dict(zip(campos, fila_convertida))

            if "lat" in doc and "lon" in doc:
                lat = doc.pop("lat", None)
                lon = doc.pop("lon", None)

                if lat is None or lon is None:
                    print(f"⚠️ Coordenadas inválidas, omitiendo fila: {fila}")
                    continue

                try:
                    doc["location"] = {
                        "lat": float(lat),
                        "lon": float(lon)
                    }
                except (ValueError, TypeError):
                    print(f"⚠️ Error al convertir lat/lon a float en fila: {fila}")
                    continue

            bulk_data += json.dumps({"index": {"_index": indice}}) + "\n"
            bulk_data += json.dumps(doc) + "\n"

    r = requests.post(f"{ELASTIC_URL}/_bulk", headers=HEADERS, data=bulk_data)
    if r.status_code == 200:
        print(f"✅ Datos cargados en índice '{indice}'")
    else:
        print(f"❌ Error al cargar '{indice}': {r.text}")


if __name__ == "__main__":
    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_comuna/part-r-00000",
        indice="eventos_por_comuna",
        campos=["comuna", "total"],
        tipos=["str", "int"]
    )

    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_dia/part-r-00000",
        indice="eventos_por_dia",
        campos=["fecha", "total"],
        tipos=["str", "int"]
    )

    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_dia_y_tipo/part-r-00000",
        indice="eventos_por_dia_y_tipo",
        campos=["fecha", "evento", "total"],
        tipos=["str", "str", "int"]
    )

    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_hora/part-r-00000",
        indice="eventos_por_hora",
        campos=["hora", "total"],
        tipos=["int", "int"]
    )

    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_hora_y_tipo/part-r-00000",
        indice="eventos_por_hora_y_tipo",
        campos=["hora", "evento", "total"],
        tipos=["int", "str", "int"]
    )

    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_tipo/part-r-00000",
        indice="eventos_por_tipo",
        campos=["evento", "total"],
        tipos=["str", "int"]
    )

    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_tipo_y_comuna/part-r-00000",
        indice="eventos_por_tipo_y_comuna",
        campos=["evento", "comuna", "total"],
        tipos=["str", "str", "int"]
    )

    cargar_csv_a_elasticsearch(
        ruta_csv="../procesador/resultados/por_ubicacion/part-m-00000",
        indice="eventos_por_ubicacion",
        campos=["evento", "lat", "lon", "comuna", "fecha", "timestamp"],
        tipos=["str", "float", "float", "str", "str", "int"]
    )
