from playwright.sync_api import sync_playwright, Error
import time
from func.utils import (
    manejar_respuesta,
    mover_mapa,
    hacer_zoom_out,
    ZOOM_OUT_NIVELES,
    movimiento_espiral,
    URL_API
)

URL_WAZE = "https://www.waze.com/es-419/live-map"

def iniciar_scraper():
    while True:
        try:
            with sync_playwright() as p:
                navegador = p.chromium.launch(headless=False)
                pagina = navegador.new_page()
                pagina.on("response", manejar_respuesta)

                print(f"🌐 Cargando {URL_WAZE}...")
                pagina.goto(URL_WAZE)

                try:
                    pagina.locator("//button[contains(text(), 'Entendido')]").click(timeout=10000)
                    print("✅ Ventana emergente cerrada.")
                except:
                    print("ℹ️ No apareció ventana emergente.")

                time.sleep(3)
                hacer_zoom_out(pagina, veces=ZOOM_OUT_NIVELES)
                time.sleep(3)

                movimientos = movimiento_espiral(niveles=5, paso=300)
                print("📡 Iniciando scraping. Ctrl+C para detener.")

                for dx, dy in movimientos:
                    mover_mapa(pagina, dx, dy)

                print("✅ Recorrido completo. Reiniciando en 60 segundos.")
                time.sleep(60)

        except Error as e:
            print(f"Error Playwright: {e}")
            print("Reiniciando tras fallo en página.")
            time.sleep(5)
        except KeyboardInterrupt:
            print("🛑 Scraping detenido.")
            break


if __name__ == "__main__":
    print(f"Scraping enviando a: {URL_API}")
    iniciar_scraper()
