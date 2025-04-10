import psutil
import subprocess
import time
import pyautogui
import os
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
SAVE_FOLDER = r"C:\path_to_save_images"  # Ajusta la ruta de guardado de imágenes

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
    time.sleep(5)  # Espera un momento para asegurarse de que Chrome se ha iniciado

# Configura las opciones para conectarse a la sesión remota de Chrome
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Conéctate a la sesión remota de Chrome
driver = webdriver.Chrome(service=Service(r"C:\Users\palma.a.guadalupe\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"), options=chrome_options)

# Abre la página (si no está ya abierta)
driver.get('https://console.firebase.google.com/project/nvabexdev/analytics/app/android:mx.com.miapp/streamview/realtime~2Foverview%3Ffpn%3D872695562182?hl=es-419')

# Espera a que el gráfico sea visible (ajusta según el id o clase de tu gráfico)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "g.bargroup")))

# Encuentra las barras de gráfico (ajusta el selector según tu caso)
bars = driver.find_elements(By.CSS_SELECTOR, "g.bargroup")

# Selecciona la segunda barra desde la derecha
bar = bars[-2]  # El índice puede cambiar según tu gráfico

# Usa ActionChains para hacer hover sobre la barra (en este caso el valor de 1 minuto)
actions = ActionChains(driver)
actions.move_to_element(bar).perform()

# Espera a que el tooltip aparezca
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='tooltip']")))

# Obtén el texto del tooltip
tooltip = driver.find_element(By.CSS_SELECTOR, "div[role='tooltip']").text

# Imprime el valor obtenido del tooltip
print("Valor del tooltip: ", tooltip)

# -------------------------------
# FUNCIÓN: Capturar un área específica de la pantalla
# -------------------------------

def capture_screen_area(x, y, width, height, file_name):
    """Captura un área específica de la pantalla y la guarda en una carpeta."""
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    file_path = os.path.join(SAVE_FOLDER, file_name)
    screenshot.save(file_path)
    print(f"📷 Imagen guardada en: {file_path}")
    return file_path

# -------------------------------
# Captura la zona de la métrica de 1 minuto (ajustar coordenadas si es necesario)
# -------------------------------

# Coordenadas y tamaño del área a capturar (ajusta según tu caso)
x, y, width, height = 965, 870, 86, 55  # Coordenadas y tamaño para capturar el área de la métrica de 1 minuto
file_name = "metrica_1_min.png"

# Captura la imagen
image_path = capture_screen_area(x, y, width, height, file_name)

# Imprime el nombre del archivo guardado
print("Imagen guardada en:", image_path)

# Cierra el navegador al final del script
driver.quit()
