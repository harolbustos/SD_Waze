import time
import random
import os
import numpy as np
from func.utils import (
    obtener_eventos,
    obtener_eventos_por_tipo,
    obtener_tipos_disponibles
)

CACHE_URL = os.getenv("CACHE_URL", "http://localhost:4000")
DELAY_FIJO = 6

# Distribución no uniforme
DISTRIBUCION_PESADA = {
    "ACCIDENT": 0.1,
    "JAM": 0.05,
    "HAZARD": 0.05,
    "POLICE": 0.8
}

def seleccionar_tipo_uniforme(tipos):
    return random.choice(tipos)

def seleccionar_tipo_no_uniforme():
    tipos = list(DISTRIBUCION_PESADA.keys())
    pesos = list(DISTRIBUCION_PESADA.values())
    return np.random.choice(tipos, p=pesos)

def esperar_exponencial(media_segundos=2):
    delay = np.random.exponential(scale=media_segundos)
    # print(f"⏱ Esperando {delay:.2f} segundos (exp)")
    time.sleep(delay)

def esperar_fijo(segundos=DELAY_FIJO):
    # print(f"⏱ Esperando {segundos} segundos (fijo)")
    time.sleep(segundos)

def esperar_normal(media=2, desviacion=0.5):
    delay = max(0.1, np.random.normal(media, desviacion))
    # print(f"⏱ Esperando {delay:.2f} segundos (normal)")
    time.sleep(delay)

def main():
    print("🚦 Generador de tráfico iniciado")

    tipos_disponibles = obtener_tipos_disponibles(CACHE_URL)
    if not tipos_disponibles:
        print("No se pudieron obtener tipos desde la API. Usando valores fijos.")
        tipos_disponibles = list(DISTRIBUCION_PESADA.keys())

    contador = 0

    while True:
        contador += 1

        # Alternar entre distribucion uniforme y no uniforme
        if contador % 2 == 0:
            print("🟢 Distribucion uniforme")
            tipo = seleccionar_tipo_uniforme(tipos_disponibles)
        else:
            print("🔵 Distribucion no uniforme")
            tipo = seleccionar_tipo_no_uniforme()

        obtener_eventos_por_tipo(CACHE_URL, tipo)

        if contador % 5 == 0:
            print("📡 Consulta general a /eventos")
            obtener_eventos(CACHE_URL)

        # Alternar entre espera fija y exponencial
        if contador % 3 == 0:
            esperar_exponencial(media_segundos=2)
        elif contador % 3 == 1:
            esperar_normal(media=2, desviacion=0.5)
        else:
            esperar_fijo()


if __name__ == "__main__":
    main()
