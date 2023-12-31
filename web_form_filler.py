# web_form_filler.py

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from datetime import datetime


def init_webdriver(chrome_driver_path, chrome_binary_path):
    driver_path = chrome_driver_path
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800,600')
    options.add_argument('window-position=100,100')
    options.binary_location = chrome_binary_path
    driver = webdriver.Chrome(options=options)
    return driver


def login(driver, username, password):
    driver.get('https://info.sirena.mx/index.php')

    # Esperar hasta que el elemento sea clickeable y realizar la acción de login
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='login']"))
    )
    username_input.send_keys(username)

    password_input = driver.find_element(
        By.CSS_SELECTOR, "input[name='password']")
    password_input.send_keys(password)

    driver.find_element(By.ID, 'go').click()

    # Esperar a que el botón de promovidos sea clickeable y hacer clic
    promovidos_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@onclick, 'window.location=\"./simpatiza.php\"')]"))
    )
    promovidos_button.click()

    # Esperar a que el botón de registrar en línea sea clickeable y hacer clic
    registrar_en_linea_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.btns.btns-ok span.ii i.fas.fa-link"))
    )
    registrar_en_linea_button.click()


def fill_web_form(driver, record):

    # Cambiar a la nueva ventana o pestaña (si es necesario)
    driver.switch_to.window(driver.window_handles[-1])

    if not pd.isna(record['telefono']):
        # Esperar hasta que el radio button sea clickeable
        simpatizante_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'xxsimpatizante1'))
        )
        simpatizante_radio_button.click()

        p_comite_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'xxc_defensa2'))
        )
        p_comite_radio_button.click()

        p_def_voto_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'xxdv_representante2'))
        )
        p_def_voto_radio_button.click()

        invit_person_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'xxinvitando1'))
        )
        invit_person_radio_button.click()

        num_invit_person_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'xxqpersonas_4t4'))
        )
        num_invit_person_radio_button.click()

        # Seleccionar la opción para "medad"
        medad_option = driver.find_element(By.ID, 'xxmedad1')
        medad_option.click()

        # Ingresar información en los campos
        nombre_input = driver.find_element(By.ID, 'nombre')
        nombre_input.send_keys(record['nombre'])

        apellidop_input = driver.find_element(By.ID, 'paterno')
        apellidop_input.send_keys(record['paterno'])

        apellidom_input = driver.find_element(By.ID, 'materno')
        apellidom_input.send_keys(record['materno'])

        if not pd.isna(record['cve_elec']):
            apellidom_input = driver.find_element(By.ID, 'cve_ife')
            apellidom_input.send_keys(record['cve_elec'])

        # Si encuentra el valor, seguir con el resto del código...
        tel_input = driver.find_element(By.ID, 'tel')
        tel_input.send_keys(record['telefono'])

    else:
       # Esperar hasta que el radio button sea clickeable
        simpatizante_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'xxsimpatizante2'))
        )
        simpatizante_radio_button.click()

    calle_input = driver.find_element(By.ID, 'calle')
    calle_input.send_keys(record['calle'])

    ext_input = driver.find_element(By.ID, 'num_ext')
    ext_input.send_keys(record['num'])

    municipio_dropdown = driver.find_element(By.ID, 'municipio')
    municipio_dropdown.send_keys(record['municipio'])

    colonia_input = driver.find_element(By.ID, 'colonia')
    colonia_input.send_keys(record['colonia'])

    if not pd.isna(record['cp']) and not pd.isna(record['telefono']):

        ext_input = driver.find_element(By.ID, 'cp')
        ext_input.send_keys(record['cp'])

    time.sleep(1)
    seccion_dropdown = driver.find_element(By.ID, 'seccion')
    seccion_dropdown.send_keys(record['seccion'])

    driver.find_element('id', 'info').click()

    # Hacer clic en el botón "Enviar/Guardar"
    enviar_guardar_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'submitokm'))
    )
    enviar_guardar_button.click()
    hay_error = False
    if not pd.isna(record['telefono']):
        driver.switch_to.window(driver.window_handles[-1])
        # Esperar a que el mensaje de error aparezca (max 5 segundos)
        try:
            # Seleccionar por direccion
            por_dir = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.ID, 'apd'))
            )
            por_dir.click()
        except TimeoutException:
            try:
                error_message = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/h1/font/span[contains(text(),'ERROR:')]"))
                )
                # Si el mensaje de error está presente, hacer clic en el botón "Volver"
                time.sleep(1)
                volver_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
                )
                volver_button.click()
                hay_error = True
                mensaje = "ERROR1: El registro se capturo anteriormente"
            except TimeoutException:
                hay_error = False
            if not hay_error:
                try:
                    # Esperar a que el mensaje de error aparezca (max 5 segundos)
                    sirena_message = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//h1[contains(., 'El simpatizante ya existe, fue registrado en info-sirena.')]"))
                    )
                    # Si el mensaje de error está presente, hacer clic en el botón "Volver"
                    time.sleep(1)
                    volver_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
                    )
                    volver_button.click()
                    hay_error = True
                    mensaje = "ERROR2: El registro ya se encuentra en sirena"
                except TimeoutException:
                    hay_error = False
            if not hay_error:
                # Esperar a que el mensaje de error aparezca (max 5 segundos)
                try:
                    error_message = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//b[contains(text(),'ERROR:')]"))
                    )
                    # Si el mensaje de error está presente, hacer clic en el botón "Volver"
                    time.sleep(1)
                    volver_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
                    )
                    volver_button.click()
                    hay_error = True
                    mensaje = "ERROR3: El registro presento un error"
                except TimeoutException:
                    hay_error = False
            if not hay_error:
                # Esperar a que el mensaje de error aparezca (max 5 segundos)
                try:
                    error_message = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/h1/font/b[contains(text(),'Dato inválido,')]"))
                    )
                    # Si el mensaje de error está presente, hacer clic en el botón "Volver"
                    time.sleep(1)
                    volver_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
                    )
                    volver_button.click()
                    hay_error = True
                    mensaje = "ERROR4: Dato Inválido"
                except TimeoutException:
                    hay_error = False

    if not hay_error:

        # Cambiar a la nueva ventana o pestaña
        driver.switch_to.window(driver.window_handles[-1])

        # Esperar 5 segundos después de abrir la nueva página
        time.sleep(1)

        # Hacer clic en el botón "Actualizar coordenadas"
        actualizar_coordenadas_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, 'actualizar'))
        )
        actualizar_coordenadas_button.click()

        # Esperar a que el botón "Cerrar" sea clickeable
        time.sleep(1)
        cerrar_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btns.btns-gris[onclick='window.close();']"))
        )
        cerrar_button.click()

        driver.switch_to.window(driver.window_handles[-1])
        # Esperar a que el botón de promovidos sea clickeable y hacer clic
        time.sleep(1)
        volver_promovidos_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@onclick, 'window.location=\"./simpatiza.php\"')]"))
        )
        volver_promovidos_button.click()

        # Esperar a que el botón de registrar en línea sea clickeable y hacer clic
        registrar_en_linea_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btns.btns-ok span.ii i.fas.fa-link"))
        )
        registrar_en_linea_button.click()
        mensaje = "Capturado"
    return mensaje


def automate_web_form(user, password, distrito, max_records, start_time, records_processed, resumen, espera, hora_ini, hora_fin, chrome_driver_path, chrome_binary_path, db_processor, update_ui_callback):
    driver = None
    mensaje = ""
    mensaje_salida = ""
    end_time = datetime.now()
    total_time = end_time - start_time
    if records_processed == 0:
        average_record_time = 0
    else:
        average_record_time = total_time / records_processed
    try:
        driver = init_webdriver(chrome_driver_path, chrome_binary_path)
        login(driver, user, password)

        while records_processed < max_records:
            now = datetime.now().time()
            # Comprobar si la hora actual está dentro del rango permitido
            if not (hora_ini <= now <= hora_fin):
                mensaje_salida = "Fuera del horario programado. Esperando..."
                update_ui_callback(resumen, start_time, end_time,
                                   total_time, average_record_time, mensaje_salida)
                print("Fuera del horario programado. Esperando...")
                # Esperar un tiempo antes de la próxima comprobación
                time.sleep(60)
                continue  # Continuar con la siguiente iteración del bucle

            mensaje_salida = "Procesando Registro..."
            update_ui_callback(resumen, start_time, end_time,
                               total_time, average_record_time, mensaje_salida)
            record = db_processor.fetch_next_record(distrito)
            if not record:
                mensaje_salida = "Automatizacion Concluida:\nNo hay más registros pendientes."
                print("No hay más registros pendientes.")
                break

            start_record_time = datetime.now()
            db_processor.update_record_start(record['id'], start_record_time)
            mensaje = fill_web_form(driver, record)
            end_time = datetime.now()
            db_processor.update_record_end(record['id'], end_time, mensaje)
            resumen['registros_procesados'] += 1
            if mensaje == "Capturado":
                resumen['registros_capturados'] += 1
            elif "ERROR" in mensaje:
                resumen['registros_omitidos'] += 1
                if "ERROR1" in mensaje:
                    resumen['registros_duplicado'] += 1
                if "ERROR2" in mensaje:
                    resumen['registros_sirena'] += 1
                if "ERROR3" in mensaje:
                    resumen['registros_error'] += 1
                if "ERROR4" in mensaje:
                    resumen['registros_error'] += 1

            # Actualizar el DataFrame con el mensaje
            if mensaje == "Capturado":
                records_processed += 1

            # Llamada al callback de actualización de la UI
            average_record_time = (end_time - start_time) / \
                resumen['registros_procesados']
            total_time = end_time - start_time
            mensaje_salida = f"Resultado: \n{mensaje}"
            update_ui_callback(resumen, start_time, end_time,
                               total_time, average_record_time, mensaje_salida)
            time.sleep(espera)  # Esperar un tiempo antes de reintentar

    except Exception as e:
        print(f"Error general en la automatización: {e}")

        if driver:
            driver.quit()
        driver = None
        # Reintentar la automatización en caso de fallo general
        if records_processed < max_records:
            print("Reintentando la automatización...")
            mensaje_salida = "Reintentando la automatización..."
            db_processor.reconnect()
            update_ui_callback(resumen, start_time, end_time,
                               total_time, average_record_time, mensaje_salida)
            time.sleep(espera)  # Esperar un tiempo antes de reintentar
            return automate_web_form(user, password, distrito, max_records, start_time, records_processed, resumen, espera, hora_ini, hora_fin, chrome_driver_path, chrome_binary_path, db_processor, update_ui_callback)

    finally:
        if driver:
            driver.quit()
        end_time = datetime.now()
        total_time = end_time - start_time
        if resumen['registros_procesados'] == 0:
            average_record_time = 0
        else:
            average_record_time = total_time / resumen['registros_procesados']
        if records_processed == max_records:
            mensaje_salida = "Automatización concluida"
        print(f"Automatización iniciada a las: {
              start_time.strftime('%H:%M:%S')}")
        print(f"Automatización finalizada a las: {
              end_time.strftime('%H:%M:%S')}")
        print(f"Duración total: {total_time}")
        update_ui_callback(resumen, start_time, end_time,
                           total_time, average_record_time, mensaje_salida)

# Función principal que se llamará desde la UI


def main(usuario, contrasena, distrito, max_records, start_time, records_processed, resumen, espera, hora_ini, hora_fin, chrome_driver_path, chrome_binary_path, db_processor, update_ui_callback):
    automate_web_form(usuario, contrasena, distrito, max_records, start_time, records_processed, resumen, espera, hora_ini, hora_fin, chrome_driver_path,
                      chrome_binary_path, db_processor, update_ui_callback)
