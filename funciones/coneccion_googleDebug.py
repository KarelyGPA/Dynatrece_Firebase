from selenium import webdriver


def coneccion_google(driver):
    # Conectar a Chrome en modo debug
    chrome_options = webdriver.ChromeOptions()
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ Conectado a Chrome en modo debug")