from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

# Conectar a Chrome en modo debug
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://console.firebase.google.com/project/nvabexdev/analytics/app/android:mx.com.miapp/streamview/realtime~2Foverview%3Ffpn%3D872695562182?hl=es-419")

time.sleep(10)
   
try:
    correo = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='VV3oRb YZVTmd SmR8']"))
    )
    correo.click()
    time.sleep(6)
except Exception as e:
    print(f"⚠ Error al encontrar el elemento: {e}")

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

try:
    mfa_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "totpPin"))
    )
    mfa_input.click()
    time.sleep(6)
    mfa_input.send_keys("Sanjuanero#Rodriguez")
    mfa_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"⚠ Error al encontrar el elemento: {e}")
    