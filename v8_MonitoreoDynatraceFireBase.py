from xml.dom.xmlbuilder import Options
import schedule
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.keys import Keys  
import time
import os
import pyautogui
import pickle
import shutil
import pytesseract
from PIL import Image
import cv2
import pygetwindow as gw
from pywinauto import Application
from datetime import datetime,timedelta
import calendar
 
#from twilio.rest import Client
# -------------------------------
# CONFIGURATION
# -------------------------------
 
# Configurar la ruta de Tesseract si es necesario
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
 
DYNATRACE_URL = "https://cdyn.mbcp.mx/login"
FIREBASE_URL = "https://console.firebase.google.com/project/nvabexdev/analytics/app/android:mx.com.miapp/streamview/realtime~2Foverview%3Ffpn%3D872695562182?hl=es-419"
DASHBOARD_URL = "https://cdyn.mbcp.mx/e/8a8f01fe-2cd3-4ce5-8ad8-93a523c5a539/#dashboard;gtf=-2h;gf=all;id=9e92fb5d-2f80-4be7-86dc-b0f001b4eb2f"
SCREENSHOT_PATH_1 = "dynatrace_dashboard.png"
SCREENSHOT_PATH_2 = "firebase_dashboard.png"
COOKIE_FILE = "session_cookies.pkl"
 
MM_path=""
counter = 0
# Grupo de WhatsApp
GROUP_NAME = "Hechiceros"  #  Nombre exacto del grupo
 
img_path = r"C:\Users\l.a.villanueva\Pictures\Capturas\dashboards.png"
#SCREENSHOT_PATH_1 = r"C:\Users\b.natali\Downloads\capturas"
#SCREENSHOT_PATH_2 = r"C:\Users\b.natali\Downloads\capturas\firebase_dashboard.png"
 
# 📂 Ruta donde se guardarán las imágenes
SAVE_FOLDER = r"C:\Users\l.a.villanueva\Pictures\Capturas"
 
# 📍 Coordenadas de las áreas a capturar Dynatrace
AREAS_TO_CAPTURE = [
    (1217, 581, 294, 60, "metricaOCP3.png"),
    (1203, 328, 347, 63, "metricaOCP4.png"),
    (23, 234, 1010, 791, "DynaGrafics.png"),
    (24, 239, 505, 252, "ocp4_grafica.png"),
    (525,239,502,250, "ocp3_grafica.png"),
]
 
AREA_TO_CAPTURE_MongoDB= (25,168,1482,859,"Captura_Mongo.png")
AREA_TO_CAPTURE_Multi= (25,168,1482,859,"Captura_Multidimencional.png")
 
# 📍 Coordenadas de las áreas a capturar Firebase
AREAS_TO_CAPTURE_Firebase = [
    (152,618,368,129, "metrica 30 min.png"),
    (161,679,278,40, "5 min.png"),
    (965,870,86, 55, "metrica 1 min.png"),
    (124,582,938,359, "dashboard.png")
]
 
# Conectar a Chrome en modo debug
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
print("✅ Conectado a Chrome en modo debug")
 
# Poner en primer plano Google
def activate_chrome():
    """Trae la ventana de Google Chrome al frente."""
    try:
        # Conéctate a la ventana de Chrome
        app = Application(backend="uia").connect(title_re=".*Google Chrome.*")
 
        # Obtiene la ventana principal de Chrome
        window = app.top_window()
 
        # Activa la ventana y la trae al frente
        window.set_focus()
       
        window.restore()
        window.maximize()
 
        print("✅ Google Chrome activado con éxito.")
    except Exception as e:
        print(f"❌ No se pudo activar Google Chrome: {e}")
 
# -------------------------------
# FUNCIÓN: Abre Dynatrace
# -------------------------------
def open_dynatrace(driver):
    """Abre Dynatrace."""
    print("\n📸 Entrando a Dynatrace...")
    driver.get(DASHBOARD_URL)
    time.sleep(20)  # Esperar carga
 
# -------------------------------
# Cerrar menu desplegado
# -------------------------------
    pyautogui.click(x=80, y=137)
    print(f"✅ Click en las coordenadas para cerrar menu")
 
# -------------------------------
# FUNCIÓN: Sacar metricas Firebase
# -------------------------------
def metricasF(driver):
    driver.get(FIREBASE_URL)
    wait=WebDriverWait(driver,20)
    try:
       
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='iframe-analytics']")))
        driver.switch_to.frame(iframe)
 
        # 2️⃣ Esperar el contenedor donde están los valores
        contenedor_valores = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//counter//div[contains(@class, 'counter-container')]")
        ))
 
        # 3. Diccionario para almacenar las métricas extraídas
        metricas =[]
 
        for contenedor in contenedor_valores:
            try:
                # Buscar el título "Usuarios activos durante los últimos 30 minutos"
                titulos = contenedor.find_elements(By.XPATH, ".//xap-text-trigger")
                time.sleep(5)
                # Extraer todos los valores dentro del contenedor
                valores = contenedor.find_elements(By.XPATH, ".//div[@class='counter']")
 
                # Asegurar que cada título tenga un valor correspondiente
                for titulo, valor in zip(titulos, valores):
                    texto_titulo = titulo.text.strip()
                    texto_valor = valor.text.strip()
 
                    if texto_titulo and texto_valor:
                        metricas.append(texto_valor)
 
            except:
                continue  # Si hay algún error en un contenedor, sigue con el siguiente
 
        print("📊 Métricas extraídas:", metricas)
        return metricas
 
    except Exception as e:
        print(f"⚠ Error al obtener las métricas: {e}")
        return None
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
# FUNCIÓN: Extraer texto de una imagen usando OCR
# -------------------------------
def extract_text_from_image(img_path):
    """Extrae el texto de una imagen usando OCR."""
    try:
        image_cv = cv2.imread(img_path)
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Mejorar contraste
        text = pytesseract.image_to_string(thresh, lang="eng")  # Extraer texto
        return text.strip()  # Eliminar espacios innecesarios
    except Exception as e:
        print(f"⚠️ Error al extraer texto de {img_path}: {e}")
        return ""
 
 
# -------------------------------
# FUNCIÓN: Abrir FireBase
# -------------------------------
def open_firebase(driver):
    """Toma una captura de pantalla de FireBase."""
    print("\n📸 Capturando FireBase...")
    driver.get(FIREBASE_URL)
    time.sleep(25)  # Esperar carga
 
 
# -------------------------------
# FUNCIÓN: juntar imagenes
# -------------------------------
def join_img(img_path):
    # Definir los paths de las imágenes fuente
    path_imagen1 = r"C:\Users\l.a.villanueva\Pictures\Capturas\DynaGrafics.png"
    path_imagen2 = r"C:\Users\l.a.villanueva\Pictures\Capturas\dashboard.png"
 
    # Abrir ambas imágenes
    imagen1 = Image.open(path_imagen1)
    imagen2 = Image.open(path_imagen2)
 
    # Obtener las dimensiones de las imágenes
    ancho1, alto1 = imagen1.size
    ancho2, alto2 = imagen2.size
 
    # Definir el ancho y altura de la imagen combinada
    ancho_final = max(ancho1, ancho2)
    alto_final = alto1 + alto2
 
    # Crear una nueva imagen con fondo blanco
    imagen_combinada = Image.new("RGB", (ancho_final, alto_final), (255, 255, 255))
 
    # Pegar ambas imágenes en la nueva imagen
    imagen_combinada.paste(imagen1, (0, 0))
    imagen_combinada.paste(imagen2, (0, alto1))
 
    # Guardar la nueva imagen en el path indicado
    imagen_combinada.save(img_path)
 
    print(f"Imagen guardada en: {img_path}")
 
#---------------------------------------
#Metricas D
#-------------------------------------
 
def metricas(driver):
    driver.get("https://cdyn.mbcp.mx/e/8a8f01fe-2cd3-4ce5-8ad8-93a523c5a539/#dashboard;id=9e92fb5d-2f80-4be7-86dc-b0f001b4eb2f;gf=all;gtf=-2h")
    try:
        wait = WebDriverWait(driver, 20)  # Espera hasta 10 segundos
        elementos = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'dTc-n') and contains(@class, 'dTc-n')]//span"))
        )
        valores = [elemento.text for elemento in elementos]
        print("Valores numéricos:", valores)
        return valores
    except Exception as e:
        print("Error al obtener los valores:", e)
        return None
#---------------------------------------
#Captura Mongo y Multidimensional
#---------------------------------------
def metricasMM(MM_path):
    driver.get("https://cdyn.mbcp.mx/e/8a8f01fe-2cd3-4ce5-8ad8-93a523c5a539/#dashboard;id=7cb4b233-65fd-4f88-93ce-01c4b1223667;gtf=-2h;gf=all")
    time.sleep(5)
    mongo_img_path=capture_screen_area(25,168,1482,859,"Captura_Mongo.png")
   
    driver.get("https://cdyn.mbcp.mx/e/8a8f01fe-2cd3-4ce5-8ad8-93a523c5a539/ui/services/SERVICE-833B44E5703F391D/mda?mdaId=exceptions&servicefilter=0%1E10%11SERVICE_METHOD_GROUP-E21290F667574BC5%14Dynamic%20web%20requests&gtf=last%202%20hours&gf=-6665196186108284696&metric=RESPONSE_TIME&dimension=All%20request%7BRelative-URL%7D&mergeServices=true&aggregation=AVERAGE&percentile=80&chart=COLUMN")
    wait = WebDriverWait(driver, 20)
    time.sleep(20)
    try:
        multi_img_path=capture_screen_area(25,168,1482,859,"Captura_Multidimencional.png")
    except Exception as e:
        print("Error al obtener los valores:", e)
        return None
   
    # Abrir ambas imágenes
    imagen1 = Image.open(mongo_img_path)
    imagen2 = Image.open(multi_img_path)
 
    # Obtener las dimensiones de las imágenes
    ancho1, alto1 = imagen1.size
    ancho2, alto2 = imagen2.size
 
    # Definir el ancho y altura de la imagen combinada
    ancho_final = max(ancho1, ancho2)
    alto_final = alto1 + alto2
 
    # Crear una nueva imagen con fondo blanco
    imagen_combinada = Image.new("RGB", (ancho_final, alto_final), (255, 255, 255))
 
    # Pegar ambas imágenes en la nueva imagen
    imagen_combinada.paste(imagen1, (0, 0))
    imagen_combinada.paste(imagen2, (0, alto1))
   
    MM_path = r"C:\Users\l.a.villanueva\Pictures\Capturas\MM.png"
    # Guardar la nueva imagen en el path indicado
    imagen_combinada.save(MM_path)
 
    print(f"Imagen guardada en: {MM_path}")
 
    return (MM_path)
 
 
#---------------------------------------
#Metricas Firebase
#-------------------------------------
def obtener_datos(url):
   
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "chart-hover-card-new"))
        )
        # Identificar las barras que contienen los datos (puedes cambiar esto dependiendo de la estructura de la página)
        barras = driver.find_elements(By.XPATH, "//*[contains(@class, 'chart-hover-card-new')]")
        # Instanciar ActionChains para simular el hover
        action = ActionChains(driver)
        # Tiempos que queremos filtrar
        tiempos_deseados = ["Hace 1 minuto", "Hace 5 minutos"]
        for barra in barras:
            # Hacer hover sobre la barra
            action.move_to_element(barra).perform()
            time.sleep(5)
            # Verificar si el bloque tiene el tiempo deseado
            for tiempo in tiempos_deseados:
                if tiempo in barra.text:
                    try:
                        # Intentar obtener el valor de usuarios activos
                        usuarios = barra.find_element(By.XPATH, ".//div[contains(@class, 'val')]").text
                        print(f"{tiempo} - Usuarios activos: {usuarios}")
                    except Exception as e:
                        print(f" Error al obtener el valor de usuarios para {tiempo}: {e}")
    except Exception as e:
        print(f"⚠ Error al obtener los datos: {e}")
# -------------------------------
# FUNCIÓN: Enviar a WhatsApp
# -------------------------------
# def send_to_whatsapp(img_path, message, group_name):  
#     message = "Usuarios en el último minuto\u000AUsuarios en los últimos 5 minutos"
 
   
#     driver.get("https://web.whatsapp.com")
 
#     time.sleep(10)
#     try:
#         search_box = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox']"))
#         )
#         search_box.click()
#         search_box.send_keys(group_name)
#         time.sleep(2)
#         search_box.send_keys(Keys.ENTER)
#         time.sleep(2)
#     except Exception as e:
#         print(f"⚠ Error al encontrar el grupo '{group_name}': {e}")
#         return
   
    # Adjuntar y enviar imágen
def send_to_whatsapp(img_path, message, group_name, valores, metricasfb,text):  
    #message = "Usuarios en el último minuto" + "*",text,"*" + "\nUsuarios en los últimos 5 minutos" + "*",metricasfb[0],"*" + "\nUsuarios en los últimos 30 minuto" + "*",metricasfb[1],"*" +  "\nApicast bex promedio 3-" + "*", valores[0], "*" +  "4- " + "*", valores[2],"*"
    message = (
    "Usuarios activos en el último minuto *" + str(text) + "*\n"
    "Usuarios en los últimos 5 minutos *" + str(metricasfb[0]) + "*\n"
    "Usuarios en los últimos 30 minutos *" + str(metricasfb[1]) + "*\n"
    "Apicast bex promedio 3- *" + str(valores[0]) + "* 4- *" + str(valores[2]) + "*"
        )
   
    driver.get("https://web.whatsapp.com")
    time.sleep(10)
   
    try:
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox']"))
        )
        search_box.click()
        search_box.send_keys(group_name)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
    except Exception as e:
        print(f"⚠ Error al encontrar el grupo '{group_name}': {e}")
        return
    try:
        attach_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-tab='10']"))
        )
        attach_button.click()
        time.sleep(2)
           
        image_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Photos & videos']/following-sibling::input[@type='file']"))
        )
        image_input.send_keys(os.path.abspath(img_path))
        time.sleep(5)
           
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        send_button.click()
        time.sleep(2)
    except Exception as e:
            print(f"⚠ Error al adjuntar imagen {img_path}")
    # Enviar el mensaje usando 'Shift + Enter' para saltos de línea
    try:
        text_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @aria-label='Type a message']"))
        )
        text_box.click()
        time.sleep(1)
 
        # Para forzar el salto de línea, reemplazamos '\n' con Keys.SHIFT + Keys.ENTER
        for line in message.split("\n"):
            text_box.send_keys(line)  # Enviar una línea
            text_box.send_keys(Keys.SHIFT + Keys.ENTER)  # Salto de línea
        text_box.send_keys(Keys.RETURN)  # Finalmente, enviar el mensaje
        time.sleep(1)
 
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        send_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"⚠ Error al enviar el mensaje: {e}")
 
    #---------------------------------
    #SI OCP3 o OCP4 es mayor a 200
    #-------------------------------
   
    metrica_OCP3=float(valores[2])
    metrica_OCP4=float(valores[0])
 
    if metrica_OCP3 > 55 and metrica_OCP4 > 55:
        #Mensaje de alerta
        message_alert = (
        "*ALERTA*, métricas OCP3 y OCP4 arriba de 200:" + "*\n" + "*OCP3* = " + "*" + str(valores[2]) + "*\n" + "*OCP4* = *" + str(valores[0]) + "*"
        )
 
    else:
        counter=0
        for valor in valores:
           
            counter=counter+1
            if counter == 1 and metrica_OCP4 > 55:
                img_path = r"C:\Users\l.a.villanueva\Pictures\Capturas\ocp4_grafica.png"
                Metrica_Alerta = "OCP4"
                valorr= valores[0]
            elif counter == 3 and metrica_OCP3 > 55:
                img_path = r"C:\Users\l.a.villanueva\Pictures\Capturas\ocp3_grafica.png"
                Metrica_Alerta = "OCP3"
                valorr= valores[2]
            else: continue
 
            try:
                valor_f = float(valorr)
                valor_i = int(valor_f)
                print("pasó por valor i: ", valor_i)
            except ValueError:
                print(f" Error al convertir '{valorr}' a número")
                continue
 
            #Mensaje de alerta
        message_alert = (
        "*ALERTA*, métricas OCP3 y OCP4 arriba de 200:" + "*\n" + "*OCP3* = " + "*" + str(valores[2]) + "*\n" + "*OCP4* = *" + str(valores[0]) + "*"
        )
 
    if metrica_OCP3 > 55 or metrica_OCP4 > 55:
        try:
            attach_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-tab='10']"))
            )
            attach_button.click()
            time.sleep(2)
           
            image_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Photos & videos']/following-sibling::input[@type='file']"))
            )
            image_input.send_keys(os.path.abspath(r"C:\Users\l.a.villanueva\Pictures\Capturas\MM.png"))
            time.sleep(5)
           
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
            )
            send_button.click()
            time.sleep(2)
        except Exception as e:
                print(f"⚠ Error al adjuntar imagen {MM_path}")
        # Enviar el mensaje usando 'Shift + Enter' para saltos de línea
        time.sleep(2)
        try:
            text_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @aria-label='Type a message']"))
            )
            text_box.click()
            time.sleep(2)
   
            # Para forzar el salto de línea, reemplazamos '\n' con Keys.SHIFT + Keys.ENTER
            for line in message_alert.split("\n"):
                text_box.send_keys(line)  # Enviar una línea
                text_box.send_keys(Keys.SHIFT + Keys.ENTER)  # Salto de línea
            text_box.send_keys(Keys.RETURN)  # Finalmente, enviar el mensaje
            time.sleep(2)
   
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
            )
            send_button.click()
            time.sleep(2)
        # try:
        #     text_box = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @aria-label='Type a message']"))
        #     )
        #     text_box.click()
        #     time.sleep(1)
   
        #     # Para forzar el salto de línea, reemplazamos '\n' con Keys.SHIFT + Keys.ENTER
        #     for line in message_alert.split("\n"):
        #         text_box.send_keys(line)  # Enviar una línea
        #         text_box.send_keys(Keys.SHIFT + Keys.ENTER)  # Salto de línea
        #     text_box.send_keys(Keys.RETURN)  # Finalmente, enviar el mensaje
        #     time.sleep(1)
   
        #     send_button = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        #     )
        #     send_button.click()
        #     time.sleep(2)
           
        except Exception as e: print("fallo el try de mandar el mensaje")
    else:
        print("no es mayor a 40 según")    
       
 
# -------------------------------
 
# FUNCTION: Send to Google Chat
 
# -------------------------------
 
def send_message_to_google_chat(driver, destinatario, message, img_path, valores, metricasfb, text):
 
    message= [
    f"Usuarios en el último minuto *{str(text)}*",
    f"Usuarios en los últimos 5 minutos *{str(metricasfb[0])}*",
    f"Usuarios en los últimos 30 minutos *{str(metricasfb[1])}*",
    f"Apicast bex promedio 3- *{str(valores[0])}* 4- *{str(valores[2])}*"
]
    driver.get("https://chat.google.com/")
 
    wait = WebDriverWait(driver, 20)
 
    try:
        # Buscar y seleccionar destinatario
 
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Buscar en el chat"]')))
 
        search_box.send_keys(destinatario)
 
        time.sleep(2)
 
        recipient = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(), "{destinatario}")]')))
 
        recipient.click()
 
        print(f"✅ Se seleccionó el chat de: {destinatario}")
 
        time.sleep(5)
 
        # Esperar a que aparezca el iframe y cambiar a él (si es necesario)
 
        try:
 
            iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@name='single_full_screen']")))
 
            driver.switch_to.frame(iframe)
 
        except:
 
            pass  # Si el iframe no aparece, continuar normalmente
 
        # Buscar el campo de mensaje
 
        mensaje_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'editable')]")))
 
        #mensaje_box.send_keys(message)
        for linea in message:
            driver.execute_script("""
        // Crea un nuevo div
        var div = document.createElement('div');
        // Agrega el texto al div
        var textNode = document.createTextNode(arguments[0]);
        div.appendChild(textNode);
        // Crea un salto de línea
        var br = document.createElement('br');
        div.appendChild(br);
        // Agrega el div al elemento padre
        arguments[1].appendChild(div);
    """, linea, mensaje_box)
 
        #driver.execute_script("arguments[0].innerHTML = arguments[1];", mensaje_box, message)
 
        mensaje_box.send_keys(Keys.RETURN)
 
        time.sleep(2)
 
        print("✅ Mensaje enviado correctamente.")
 
        # Enviar imágenes si existen
        if img_path:              
            if not os.path.exists(img_path):
                print(f"⚠️ La imagen '{img_path}' no existe.")  
            try:
                # Hacer clic en el botón de adjuntar archivo
                attach_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Subir archivo"]')))
                driver.execute_script("arguments[0].click();", attach_button)
                time.sleep(3)
                # Esperar input de archivo y subir la imagen
                file_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
                file_input.send_keys(os.path.abspath(img_path))
                print(f"📂 Imagen '{img_path}' seleccionada para enviar.")
                time.sleep(5)  # Esperar subida
                # 🔹 Cerrar ventana de explorador de archivos
                pyautogui.press("esc")  # Intentar con ESC
                time.sleep(1)
                print("❎ Intentando cerrar ventana de explorador de archivos.")
                # Enviar la imagen
                send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enviar mensaje']")))
                driver.execute_script("arguments[0].click();", send_button)
                print(f"✅ Imagen enviada: {img_path}")
                time.sleep(5)
            except Exception as img_error:
                print(f"❌ Error al adjuntar la imagen '{img_path}': {img_error}")
 
    except Exception as e:
        print(f"❌ Error en el proceso: {e}")
   
 
    #------------------------------#
     #SI OCP3 o OCP4 es mayor a 200
   
    metrica_OCP3=float(valores[2])
    metrica_OCP4=float(valores[0])
 
    if metrica_OCP3 > 55 and metrica_OCP4 > 55:
        #Mensaje de alerta
            message_alert_google= [
        f"*ALERTA*, métricas OCP3 Y OCP4 arriba de 200:",
        f"*OCP3* = *{str(valores[2])}*",
        f"*OCP4* = *{str(valores[0])}*"
        ]
 
    else:
        counter=0
        for _ in valores:
           
            counter=counter+1
            if counter == 1 and metrica_OCP4 > 55:
                img_path = r"C:\Users\l.a.villanueva\Pictures\Capturas\ocp4_grafica.png"
                Metrica_Alerta = "OCP4"
                valorr= valores[0]
            elif counter == 3 and metrica_OCP3 > 55:
                img_path = r"C:\Users\l.a.villanueva\Pictures\Capturas\ocp3_grafica.png"
                Metrica_Alerta = "OCP3"
                valorr= valores[2]
            else: continue
 
            try:
                valor_f = float(valorr)
                valor_i = int(valor_f)
                print("pasó por valor i: ", valor_i)
            except ValueError:
                print(f" Error al convertir '{valorr}' a número")
                continue
 
            #Mensaje de alerta
            message_alert_google= [
        f"*ALERTA*, métrica {str(Metrica_Alerta)} arriba de 200:",
        f"*{str(Metrica_Alerta)}* = *{str(valor_i)}*"
    ]
       
        #---------------------------
        #   Enviar mensaje de alerta por Google
 
    if  metrica_OCP3 > 55 or metrica_OCP4 > 55:
 
        try:
            # Hacer clic en el botón de adjuntar archivo
            attach_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Subir archivo"]')))
            driver.execute_script("arguments[0].click();", attach_button)
            time.sleep(3)
            # Esperar input de archivo y subir la imagen
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
            file_input.send_keys(os.path.abspath(r"C:\Users\l.a.villanueva\Pictures\Capturas\MM.png"))
            print(f"📂 Imagen '{r"C:\Users\l.a.villanueva\Pictures\Capturas\MM.png"}' seleccionada para enviar.")
            time.sleep(5)  # Esperar subida
            # 🔹 Cerrar ventana de explorador de archivos
            pyautogui.press("esc")  # Intentar con ESC
            time.sleep(1)
            print("❎ Intentando cerrar ventana de explorador de archivos.")
            # Enviar la imagen
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enviar mensaje']")))
            driver.execute_script("arguments[0].click();", send_button)
            print(f"✅ Imagen enviada: {MM_path}")
            time.sleep(5)
 
        except Exception as e:
            print(f"❌ Error en el proceso: {e}")
   
 
        # Buscar el campo de mensaje
        mensaje_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'editable')]")))
 
        #mensaje_box.send_keys(message)
        for linea in message_alert_google:
            driver.execute_script("""
        // Crea un nuevo div
        var div = document.createElement('div');
        // Agrega el texto al div
        var textNode = document.createTextNode(arguments[0]);
        div.appendChild(textNode);
        // Crea un salto de línea
        var br = document.createElement('br');
        div.appendChild(br);
        // Agrega el div al elemento padre
        arguments[1].appendChild(div);
    """, linea, mensaje_box)
 
        #driver.execute_script("arguments[0].innerHTML = arguments[1];", mensaje_box, message)
 
        mensaje_box.send_keys(Keys.RETURN)
 
        time.sleep(2)
 
 
# -------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------
def main():
    print("\n🚀 Iniciando proceso de captura y envío...")  
    activate_chrome()

    try:
        valores = metricas(driver)
    except Exception as e:
        print(f"⚠️ Error al extraer métricas de Dynatrace: {e}")
        print("\n✅ Proceso finalizado con éxito.")
    
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"📂 Carpeta creada: {SAVE_FOLDER}")

    captured_images = []
    extracted_texts = {}
    extracted_texts_firebase = {}

    for (x, y, width, height, file_name) in AREAS_TO_CAPTURE:
        try:
            image_path = capture_screen_area(x, y, width, height, file_name)
            captured_images.append(image_path)
        except Exception as e:
            print(f"❌ Error al capturar {file_name}: {e}")  

    metricasMM(MM_path)

    metricasfb = metricasF(driver)

    pyautogui.moveTo(807, 843, duration=0.5)

    for (x, y, width, height, file_name) in AREAS_TO_CAPTURE_Firebase:
        try:
            img_path = capture_screen_area(x, y, width, height, file_name)
            captured_images.append(img_path)
            if "metrica" in file_name:
                text = extract_text_from_image(img_path)
                extracted_texts_firebase[file_name] = text
        except Exception as e:
            print(f"❌ Error al capturar {file_name}: {e}")

    join_img(img_path)

    message = (
        "Usuarios en el último minuto *" + str(text) + "*\n"
        "Usuarios en los últimos 5 minutos *" + str(metricasfb[0]) + "*\n"
        "Usuarios en los últimos 30 minutos *" + str(metricasfb[1]) + "*\n"
        "Apicast bex promedio 3- *" + str(valores[0]) + "* 4- *" + str(valores[2]) + "*"
    )

    send_to_whatsapp(img_path, message , GROUP_NAME, valores, metricasfb, text)

    image_paths = [SAVE_FOLDER]
    destinatario = "SRE"
    send_message_to_google_chat(driver, destinatario, message, img_path, valores, metricasfb, text)

# -------------------------------
# FUNCIÓN PARA PROGRAMAR LA EJECUCIÓN
# -------------------------------
def es_dia_excepcion():
    hoy = datetime.today()
    dia = hoy.day
    mes = hoy.month
    anio = hoy.year
    dia_semana = hoy.weekday()  # 0 = lunes, 6 = domingo

    # Verificar si el día 15 cae en lunes o martes
    dia_15 = datetime(anio, mes, 15)
    es_15_lunes_martes = dia_15.weekday() in [0, 1]  # lunes o martes

    # Verificar si el último día del mes cae en lunes o martes
    ultimo_dia_num = calendar.monthrange(anio, mes)[1]
    dia_ultimo = datetime(anio, mes, ultimo_dia_num)
    es_ultimo_lunes_martes = dia_ultimo.weekday() in [0, 1]

    # Determinar penúltimo día
    dia_penultimo = datetime(anio, mes, ultimo_dia_num - 1)

    # Determinar si hoy es 14, 15 o 16
    dias_cercanos_al_15 = dia in [14, 15, 16]
    # Determinar si hoy es penúltimo, último o primero
    es_ultimo_o_penultimo = hoy.day in [ultimo_dia_num, ultimo_dia_num - 1]
    es_primero = hoy.day == 1

    excepcion_por_15 = es_15_lunes_martes and dias_cercanos_al_15
    excepcion_por_ultimo = es_ultimo_lunes_martes and (es_ultimo_o_penultimo or es_primero)

    return excepcion_por_15 or excepcion_por_ultimo

def programar_ejecucion():
    schedule.clear()

    if es_dia_excepcion():
        print("Día de excepción: ejecutando cada 30 minutos.")
        schedule.every(30).minutes.do(main)
    else:
        dia_semana = datetime.today().weekday()
        if dia_semana <= 3:  # lunes a jueves
            print("Día normal entre semana: ejecutando cada 1 hora.")
            schedule.every().hour.do(main)
        else:  # viernes a domingo
            print("Fin de semana: ejecutando cada 30 minutos.")
            schedule.every(30).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Revisa cada minuto por eficiencia
        # Revalidar el día para adaptarse a cambios de día sin reiniciar el script
        if datetime.now().minute == 0:  # Solo a la hora exacta reprograma
            programar_ejecucion()
            break  # Salir del bucle actual para reiniciar la programación


# -------------------------------
# EJECUTAR EL SCRIPT
# -------------------------------
if __name__ == "__main__":
    programar_ejecucion()