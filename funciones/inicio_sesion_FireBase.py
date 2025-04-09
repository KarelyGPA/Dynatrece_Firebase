# -------------------------------
# Configuración de login de FireBase
# -------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

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
