import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from coneccion_googleDebug import coneccion_google
from variable import CONTACTO, MENSAJE, MENSAJE_CONFIRMACION, driver

def envio_codigoV(driver,codigo):

    # Esperar a que el campo de búsqueda esté visible
    search_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @data-tab='3']"))
    )
    search_input.clear()
    search_input.send_keys(CONTACTO)
    time.sleep(1)  # pequeña pausa para que aparezcan resultados
    search_input.send_keys(Keys.ENTER)

    # Enviar mensaje
    input_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//footer//div[@contenteditable='true']"))
    )
    input_box.send_keys(MENSAJE)
    input_box.send_keys(Keys.ENTER)
    print("📩 Mensaje enviado. Esperando código...")

    # Esperar y capturar código
    codigo = None
    timeout = time.time() + 300  # 5 minutos
    while time.time() < timeout:
        try:
            # Buscar los últimos mensajes, incluyendo el código
            mensajes = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]//span[@dir='auto']")
            for msg in reversed(mensajes[-2:]):  # últimos 5 mensajes recibidos
                texto = msg.text.strip()
                print(f"🔍 Mensaje encontrado: {texto}")  # Esto te ayudará a ver qué mensaje está leyendo
                match = re.search(r"\b\d{6}\b", texto)  # Buscar código de 6 dígitos
                if match:
                    codigo = match.group()
                    print(f"✅ Código recibido: {codigo}")
                    # Enviar confirmación de que el código ha sido tomado
                    input_box.send_keys(MENSAJE_CONFIRMACION)
                    input_box.send_keys(Keys.ENTER)
                    print("📩 Confirmación enviada: Código tomado.")
                    break
        except Exception as e:
            print(f"⚠️ Error: {str(e)}")


        if codigo:
            break

        time.sleep(5)

    if not codigo:
        print("⏰ No se recibió ningún código en 5 minutos.")
                
    return codigo

 
