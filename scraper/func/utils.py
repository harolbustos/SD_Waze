import requests
import os
import time

# Configuracion
CENTRO_X = 800
CENTRO_Y = 400
DELAY_MOVIMIENTO = 5
ZOOM_OUT_NIVELES = 5
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

def hacer_zoom_out(pagina, veces=ZOOM_OUT_NIVELES):
    for _ in range(veces):
        pagina.keyboard.press("Control+-")
        time.sleep(0.5)

def mover_mapa(pagina, dx, dy):
    x1 = CENTRO_X
    y1 = CENTRO_Y
    x2 = x1 + dx
    y2 = y1 + dy

    pagina.mouse.move(x1, y1)
    pagina.mouse.down()
    pagina.mouse.move(x2, y2, steps=20)
    pagina.mouse.up()

    time.sleep(DELAY_MOVIMIENTO)

def movimiento_espiral(niveles=6, paso=250):
    movimientos = []
    x, y = 0, 0
    dx, dy = paso, 0
    pasos = 1

    for _ in range(niveles):
        for _ in range(2):
            for _ in range(pasos):
                x += dx
                y += dy
                movimientos.append((x, y))
            dx, dy = -dy, dx
        pasos += 1

    return movimientos