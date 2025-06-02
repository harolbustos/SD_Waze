import requests
import os
import time

# Configuracion
DELAY_MOVIMIENTOS = 5
DISTANCIA_PIXELES = 200
URL_API = os.getenv("URL_API", "http://localhost:8080/eventos")
eventos_vistos = set()

def limpiar_evento(evento):
    campos_ignorados = [
        "reportDescription", "comments", "reportBy", "wazeData", "nThumbsUp",
        "reportByMunicipalityUser", "reportRating", "reportMood", "additionalInfo",
        "fromNodeId", "toNodeId", "magvar"
    ]
    for campo in campos_ignorados:
        evento.pop(campo, None)
    return evento

def enviar_evento(evento):
    try:
        r = requests.post(URL_API, json=evento)
        r.raise_for_status()
        print(f"Evento {evento.get('uuid')} enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar evento {evento.get('uuid')}: {e}")

def manejar_respuesta(response):
    if "georss" in response.url and response.status == 200:
        try:
            contenido = response.json()
            nuevos = 0
            for alerta in contenido.get("alerts", []):
                uuid = alerta.get("uuid")
                if uuid and uuid not in eventos_vistos:
                    evento_limpio = limpiar_evento(alerta)
                    eventos_vistos.add(uuid)
                    enviar_evento(evento_limpio)
                    nuevos += 1
            if nuevos > 0:
                print(f"{nuevos} eventos nuevos.")
        except Exception as e:
            print(f"Error al procesar respuesta: {e}")

def mover_mapa(page):
    movimientos = [
        ("→", 800, 400, 600, 400),
        ("↓", 800, 400, 800, 550),
        ("←", 800, 400, 1000, 400),
        ("↑", 800, 400, 800, 250),
    ]
    for nombre, x1, y1, x2, y2 in movimientos:
        page.mouse.move(x1, y1)
        page.mouse.down()
        page.mouse.move(x2, y2, steps=15)
        page.mouse.up()
        time.sleep(DELAY_MOVIMIENTOS)