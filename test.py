import psutil
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Rutas de tu instalación de Chrome y del perfil de depuración
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
debug_profile_path = r"C:\chrome_debug"

# Verifica si hay un proceso de Chrome ejecutándose
def is_chrome_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            return True
    return False

# Si Chrome no está corriendo, lo iniciamos en modo depuración remota
if not is_chrome_running():
    print("Chrome no está corriendo. Iniciando con depuración remota...")
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222", f"--user-data-dir={debug_profile_path}"])
    time.sleep(10)  # Aumentamos el tiempo de espera para asegurarnos de que Chrome se ha iniciado correctamente

# Configura las opciones para conectarse a la sesión remota de Chrome
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Conéctate a la sesión remota de Chrome
driver = webdriver.Chrome(service=Service(r"C:\Users\palma.a.guadalupe\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"), options=chrome_options)

# Abre la página (si no está ya abierta)
driver.get('https://console.firebase.google.com/project/nvabexdev/analytics/app/android:mx.com.miapp/streamview/realtime~2Foverview%3Ffpn%3D872695562182?hl=es-419')

# Espera a que el gráfico sea visible (ajusta según el id o clase de tu gráfico)
try:
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "g.bargroup")))
except Exception as e:
    print(f"⚠️ Error al esperar el gráfico: {e}")
    driver.quit()

# Encuentra las barras de gráfico (ajusta el selector según tu caso)
bars = driver.find_elements(By.CSS_SELECTOR, "g.bargroup")

# Asegúrate de que hay suficientes barras en el gráfico
if len(bars) >= 2:
    # Selecciona la segunda barra desde la derecha
    bar = bars[-2]  # El índice puede cambiar según tu gráfico

    # Usa ActionChains para hacer hover sobre la barra
    actions = ActionChains(driver)
    actions.move_to_element(bar).perform()
    print("🖱️ Moviendo el cursor sobre la barra...")

    # Espera a que el tooltip aparezca
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='tooltip']")))
        tooltip = driver.find_element(By.CSS_SELECTOR, "div[role='tooltip']").text
        print("Valor del tooltip: ", tooltip)
    except Exception as e:
        print(f"⚠️ Error al obtener el tooltip: {e}")
else:
    print("⚠️ No se encontraron suficientes barras en el gráfico.")

# Nuevo: Esperar y extraer el valor de "Usuarios activos" en el último minuto
try:
    # XPath para encontrar el valor de "Usuarios activos" en el último minuto
    usuario_xpath = "//ga-card-content//ga-panel//ga-bar-chart//ga-chart-hover-card//ga-chart-metric//div[contains(@class, 'name') and text()='Usuarios activos']//following-sibling::div[contains(@class, 'val')]"
    
    # Esperar hasta que el valor esté visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, usuario_xpath))
    )
    
    # Extraer y mostrar el valor
    usuarios_activos = driver.find_element(By.XPATH, usuario_xpath).text
    print(f"Usuarios activos en el último minuto: {usuarios_activos}")
except Exception as e:
    print(f"⚠️ Error al obtener el valor de usuarios activos: {e}")

# Mueve el cursor a las coordenadas específicas (965, 870)
actions.move_by_offset(965, 870).perform()
time.sleep(1)  # Espera un segundo para asegurarse de que el movimiento del cursor sea visible

# Captura la pantalla en las coordenadas (965, 870, 86, 55)
driver.save_screenshot("metrica_1_min.png")
print("Captura tomada y guardada como 'metrica_1_min.png'")


