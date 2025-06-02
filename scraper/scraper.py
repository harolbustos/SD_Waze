from playwright.sync_api import sync_playwright, Error as PlaywrightError
import time
import os
from func.utils import manejar_respuesta, mover_mapa


URL_API = os.getenv("URL_API", "http://localhost:8080/eventos")
URL_WAZE = "https://www.waze.com/es-419/live-map"

def iniciar_scraper():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        pagina.on("response", manejar_respuesta)

        print(f"🌐 Cargando {URL_WAZE}...")
        pagina.goto(URL_WAZE)

        # Cerrar ventana emergente
        try:
            pagina.locator("//button[contains(text(), 'Entendido')]").click(timeout=10000)
            print("Ventana emergente cerrada.")
        except:
            print("No apareció ventana emergente.")

        time.sleep(10)

        print("Iniciando scraping. Presiona Ctrl+C para detener.")
        try:
            while True:
                mover_mapa(pagina)
        except KeyboardInterrupt:
            print("🛑 Scraping detenido por el usuario.")

        except PlaywrightError as e:
            print(f"❌ Error con Playwright: {e}")

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")

        finally:
            try:
                navegador.close()
                print("🧹 Navegador cerrado correctamente.")
            except:
                print("⚠️ No se pudo cerrar el navegador (posiblemente ya estaba cerrado).")


if __name__ == "__main__":
    print(f"Scraping enviando a: {URL_API}")
    iniciar_scraper()
