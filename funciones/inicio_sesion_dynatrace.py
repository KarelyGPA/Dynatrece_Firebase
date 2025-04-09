import pickle
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from coneccion_googleDebug import coneccion_google
from v8_MonitoreoDynatraceFireBase import COOKIE_FILE, DYNATRACE_URL
from variable import DASHBOARD_URL, PASSWORD, USERNAME
# -------------------------------
# Configuración de login de Dynatrace
# -------------------------------

def ensure_logged_in():
    
    DYNATRACE_URL = "https://cdyn.mbcp.mx/e/8a8f01fe-2cd3-4ce5-8ad8-93a523c5a539/#dashboard;id=9e92fb5d-2f80-4be7-86dc-b0f001b4eb2f;gf=all;gtf=-2h"

    #URL LOG IN: https://cdyn.mbcp.mx/login

    # Configurar conexión al Chrome ya abierto en modo debug
    options = Options()
    options.debugger_address = "127.0.0.1:9222"  # Esto se conecta al Chrome abierto en modo debug
    
    # Conectarse al navegador
    driver = webdriver.Chrome(options=options)

    # # Ir a Gmail
    driver.get(DYNATRACE_URL)
    time.sleep(5)
    
    # # Verificar si ya está logueado
    # if "https://cdyn.mbcp.mx/e/8a8f01fe-2cd3-4ce5-8ad8-93a523c5a539/#dashboard;id=9e92fb5d-2f80-4be7-86dc-b0f001b4eb2f;gf=all;gtf=-2h" in driver.current_url:
    #     print("✅ Sesión iniciada en Gmail.")
    # else:
    #     print("⚠️ Sesión NO iniciada.")
    
    try:
        # Intentar encontrar el primer elemento
        user = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "user"))
        )
        user.click()
        user.send_keys(USERNAME)

    except Exception as e:
        print(f"⚠ No se encontró el primer elemento y no se escribió user: {e}")

    try:
        pswd= WebDriverWait(driver, 20).until(
            #EC.presence_of_element_located((By.XPATH, "//div[@]class='whsOnd zHQkBf']"))
            EC.presence_of_element_located((By.NAME, "pass"))
        )
        pswd.click()
        pswd.send_keys(PASSWORD)
        pswd.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"⚠ Error al encontrar el elemento: {e}")

#ensure_logged_in()
