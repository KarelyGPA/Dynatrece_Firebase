import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WHATSAPP_URL = "https://web.whatsapp.com/"




# URL de WhatsApp Web

def check_whatsapp_login(driver):
    """Verifica si la sesión está activa en WhatsApp Web."""
    
    try:
        # Esperar a que el botón de nuevo chat esté visible, lo que indica que ya se ha iniciado sesión
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-icon='chat']"))
        )
        print("✅ Sesión iniciada en WhatsApp Web.")
        return True
    except:
        print("❌ No hay sesión activa. Escanea el código QR.")
        return False

def login_to_whatsapp(driver):
    """Inicia sesión en WhatsApp Web si no está iniciada la sesión."""
    
    driver.get(WHATSAPP_URL)  # Abrir WhatsApp Web
    
    # Verificar si la sesión ya está iniciada
    if not check_whatsapp_login(driver):
        print("Esperando que escanees el código QR...")
        # Esperar el tiempo de escaneo del código QR (puedes ajustar el tiempo si es necesario)
        time.sleep(60)  # Aquí es donde el usuario tiene 60 segundos para escanear el código QR
        
        # Volver a verificar si la sesión se ha iniciado
        if check_whatsapp_login(driver):
            print("✅ Código QR escaneado correctamente.")
        else:
            print("⏰ Tiempo de escaneo agotado, no se escaneó el código QR.")
    
    # Mostrar los chats
    print("🟢 Mostrando los chats disponibles:")
    chats = driver.find_elements(By.XPATH, "//span[@class='_3lYpZ']")  # Ajusta el XPath si es necesario
    for chat in chats:
        print(f"- {chat.text}")

# Configuración de Chrome en modo debug
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"  # Conéctate al Chrome que está en modo debug
driver = webdriver.Chrome(options=chrome_options)

print("✅ Conectado a Chrome en modo debug")

# Verificar y realizar login a WhatsApp Web
login_to_whatsapp(driver)
