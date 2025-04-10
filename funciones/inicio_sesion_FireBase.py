from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

# -------------------------------
# Configuración de login de FireBase
# -------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from envio_codigo import envio_codigoV


def inicio_firebase():
    FIREBASE_URL = "https://console.firebase.google.com/project/nvabexdev/analytics/app/android:mx.com.miapp/streamview/realtime~2Foverview%3Ffpn%3D872695562182?hl=es-419"


    # Configurar conexión al Chrome ya abierto en modo debug
    options = Options()
    options.debugger_address = "127.0.0.1:9222"  # Esto se conecta al Chrome abierto en modo debug
    
    # Conectarse al navegador
    driver = webdriver.Chrome(options=options)

    # Ir a Gmail
    driver.get(FIREBASE_URL)
    time.sleep(5)
    
    # Verificar si ya está logueado
    if "https://console.firebase.google.com/project/nvabexdev/analytics/" in driver.current_url:
        print("✅ Sesión iniciada en Gmail.")
    else:
        print("⚠️ Sesión NO iniciada.")
    
        try:
            # Intentar encontrar el primer elemento
            correo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='VV3oRb YZVTmd SmR8']"))
            )
            correo.click()
            time.sleep(6)

        except Exception as e:
            print(f"⚠ No se encontró el primer elemento: {e}")
            try:
                # Intentar con el segundo elemento como alternativa
                boton_siguiente = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='O1Slxf']//button[.//span[text()='Siguiente']]"))
                )
                boton_siguiente.click()
                time.sleep(6)
            
            except Exception as e2:
                print(f"❌ Tampoco se encontró el segundo elemento: {e2}")

        try:
            search_box = WebDriverWait(driver, 20).until(
                #EC.presence_of_element_located((By.XPATH, "//div[@]class='whsOnd zHQkBf']"))
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            search_box.click()
            time.sleep(6)
            search_box.send_keys("Sanjuanero#Rodriguez")
            search_box.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"⚠ Error al encontrar el elemento: {e}")

        #---------------------------------
        # funcion de mandar codigo whats
        #---------------------------------
        # Conectar a Chrome en modo depuración
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # Crear el driver (sin abrir nueva ventana)
        driver = webdriver.Chrome(options=chrome_options)

        # Firebase ya debería estar abierto en esa sesión
        ventanaFirebase = driver.current_window_handle
        print(f"Ventana actual: {ventanaFirebase}")

        # Abre nueva pestaña
        driver.execute_script("window.open('https://web.whatsapp.com/', '_blank');")
        time.sleep(2)

        # Cambia a la nueva pestaña
        ventanas = driver.window_handles
        for handle in ventanas:
            if handle != ventanaFirebase:
                ventanaWhatsApp = handle
                driver.switch_to.window(ventanaWhatsApp)
                break

        # Espera o interactúa en WhatsApp
        codigo = ""
        while True:
            codigo = envio_codigoV(driver,codigo)
            time.sleep(5)

            # Cierra la pestaña de WhatsApp
            driver.close()

            # Regresa a la pestaña de Firebase
            driver.switch_to.window(ventanaFirebase)
            print("🔁 De vuelta en Firebase")

            try:
                mfa_input = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "totpPin"))
                )
                mfa_input.click()
                time.sleep(6)
                mfa_input.send_keys(codigo)
                mfa_input.send_keys(Keys.ENTER)    

                time.sleep(2)
            except Exception as e:
                print(f"⚠ Error al encontrar el elemento: {e}")
            
            if "https://console.firebase.google.com/project/nvabexdev/analytics/" in driver.current_url:
                break


            
