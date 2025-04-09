import pickle
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from v8_MonitoreoDynatraceFireBase import COOKIE_FILE, DYNATRACE_URL
from variable import DASHBOARD_URL, PASSWORD, USERNAME
# -------------------------------
# Configuración de login de Dynatrace
# -------------------------------

def ensure_logged_in():
    """Verifica si la sesión está activa, si no lo está, realiza login automáticamente."""
    
    def login(driver):
        """Realiza el login y guarda las cookies."""
        print("\nIniciando sesión en Dynatrace...")
        driver.get(DYNATRACE_URL)
        time.sleep(15)  # Esperar a que la página cargue completamente
        
        # 2. Ingresar usuario y contraseña con WebDriverWait
        try:
            # Esperar a que los campos estén visibles
            user_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "user"))
            )
            pass_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            
            # Ingresar los datos
            user_input.send_keys(USERNAME)
            pass_input.send_keys(PASSWORD)
            pass_input.send_keys(Keys.RETURN)

            # Esperar a que se complete el login
            time.sleep(8)
            
            # Guardar cookies después de iniciar sesión
            pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
            print("Cookies guardadas correctamente.")
        
        except Exception as e:
            print(f"Error en el login: {e}")

    def load_cookies(driver):
        """Carga cookies si están disponibles y válidas."""
        if os.path.exists(COOKIE_FILE):
            try:
                driver.get(DASHBOARD_URL)  # Ir al dashboard para verificar si la sesión es válida
                cookies = pickle.load(open(COOKIE_FILE, "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()  # Refrescar para aplicar cookies
                time.sleep(5)  # Esperar que el refresco termine
                # Verificar si las cookies son válidas comprobando un elemento específico del dashboard
                if is_logged_in(driver):
                    print("Cookies cargadas correctamente, sesión activa.")
                    return True
                else:
                    print("Las cookies no son válidas, realizando login.")
                    return False
            except Exception as e:
                print(f"Error cargando cookies: {e}")
                return False
        return False

    def is_logged_in(driver):
        """Verifica si el usuario está logueado mediante la existencia de un elemento específico."""
        try:
            # Cambia este XPath para verificar algún elemento específico en el dashboard
            driver.find_element(By.XPATH, "//div[@class='dashboard-identifier']")  # Cambia este XPath a algo específico del dashboard
            return True
        except:
            return False

    # Conectar a Chrome en modo debug
    chrome_options = webdriver.ChromeOptions()
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ Conectado a Chrome en modo debug")

    # Verificar si ya estamos logueados. Si no, realiza el login
    if not load_cookies(driver):  # Si no se cargaron las cookies correctamente o no están disponibles
        login(driver)  # Realiza el login

    return driver  # Devuelve el driver listo para continuar con la automatización

# Uso de la función
driver = ensure_logged_in()  # Llama a la función para asegurarte de que la sesión esté iniciada
