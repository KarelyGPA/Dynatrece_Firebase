import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import calendar
import schedule
import time
from datetime import datetime,timedelta
import pyautogui
import random
import os
import random
from selenium import webdriver
from inicio_sesion_FireBase import inicio_firebase
from inicio_sesion_dynatrace import ensure_logged_in
from v8_MonitoreoDynatraceFireBase import AREAS_TO_CAPTURE, GROUP_NAME, SAVE_FOLDER, AREAS_TO_CAPTURE_Firebase, MM_path, activate_chrome, capture_screen_area, extract_text_from_image, join_img, metricas, metricasF, metricasMM, send_message_to_google_chat, send_to_whatsapp

# -------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------
# Conectar a Chrome en modo debug
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
print("✅ Conectado a Chrome en modo debug")

def main():
    while True:
        try:
            print("\n🚀 Iniciando proceso de inicios de sesion...")  
            activate_chrome()
            ensure_logged_in()
            inicio_firebase()

            print("\n🚀 Iniciando proceso de capturas y envios ...")  
            try:
                valores = metricas(driver)
            except Exception as e:
                print(f"⚠️ Error al extraer métricas de Dynatrace: {e}")
                return  # Si esta métrica es crítica, termina aquí

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

            send_to_whatsapp(img_path, message, GROUP_NAME, valores, metricasfb, text)
            send_message_to_google_chat(driver, "SRE", message, img_path, valores, metricasfb, text)

            break  # Si todo sale bien, se rompe el while y no se repite
        except Exception as e:
            print(f"\n🔁 Error general en main(): {e}")
            print("🔄 Reintentando en 10 segundos...\n")
            time.sleep(10)

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
    ultima_configuracion = None
    screen_width, screen_height = pyautogui.size()

    while True:
        # Verifica si debe reconfigurar
        nueva_config = "excepcion" if es_dia_excepcion() else (
            "hora" if datetime.today().weekday() <= 3 else "30min"
        )

        if nueva_config != ultima_configuracion:
            schedule.clear()
            if nueva_config == "excepcion":
                print("🟡 Día de excepción: ejecutando cada 30 minutos.")
                schedule.every(30).minutes.do(main)
            elif nueva_config == "hora":
                print("🔵 Día normal entre semana: ejecutando cada 1 hora.")
                schedule.every().hour.do(main)
            else:
                print("🟢 Fin de semana: ejecutando cada 30 minutos.")
                schedule.every(30).minutes.do(main)

            # Ejecutar inmediatamente
            main()
            ultima_configuracion = nueva_config

        # 🖱️ Mover cursor a una posición aleatoria cada minuto
        rand_x = random.randint(0, screen_width - 1)
        rand_y = random.randint(0, screen_height - 1)
        pyautogui.moveTo(rand_x, rand_y, duration=0.5)

        schedule.run_pending()
        time.sleep(60)

# -------------------------------
# EJECUTAR EL SCRIPT
# -------------------------------
if __name__ == "__main__":
    programar_ejecucion()