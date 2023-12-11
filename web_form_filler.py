# web_form_filler.py
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd


def init_webdriver(chrome_driver_path, chrome_binary_path):
    driver_path = chrome_driver_path
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
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

    if not pd.isna(record['Telefono']):
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
        nombre_input.send_keys(record['Nombre'])

        apellidop_input = driver.find_element(By.ID, 'paterno')
        apellidop_input.send_keys(record['Paterno'])

        apellidom_input = driver.find_element(By.ID, 'materno')
        apellidom_input.send_keys(record['Materno'])

        if not pd.isna(record['CVE_ELEC']):
            apellidom_input = driver.find_element(By.ID, 'cve_ife')
            apellidom_input.send_keys(record['CVE_ELEC'])

        # Si encuentra el valor, seguir con el resto del código...
        tel_input = driver.find_element(By.ID, 'tel')
        tel_input.send_keys(record['Telefono'])

    else:
       # Esperar hasta que el radio button sea clickeable
        simpatizante_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'xxsimpatizante2'))
        )
        simpatizante_radio_button.click()

    calle_input = driver.find_element(By.ID, 'calle')
    calle_input.send_keys(record['Calle'])

    ext_input = driver.find_element(By.ID, 'num_ext')
    ext_input.send_keys(record['Num'])

    municipio_dropdown = driver.find_element(By.ID, 'municipio')
    municipio_dropdown.send_keys(record['Municipio'])

    colonia_input = driver.find_element(By.ID, 'colonia')
    colonia_input.send_keys(record['Colonia'])

    if not pd.isna(record['CP']) and not pd.isna(record['Telefono']):

        ext_input = driver.find_element(By.ID, 'cp')
        ext_input.send_keys(record['CP'])

    time.sleep(1)
    seccion_dropdown = driver.find_element(By.ID, 'seccion')
    seccion_dropdown.send_keys(record['Seccion'])

    # Verificar si el valor ingresado está presente en el campo
    # try:
    #     # Esperar hasta que el elemento con el valor ingresado aparezca
    #     WebDriverWait(driver, 2).until(
    #         EC.text_to_be_present_in_element((By.XPATH, '//*[@id="seccion"]'), seccion)
    #     )

    # Hacer clic en cualquier parte de la página
    driver.find_element('id', 'info').click()

    # Hacer clic en el botón "Enviar/Guardar"
    enviar_guardar_button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, 'submitokm'))
    )
    enviar_guardar_button.click()
    hay_error = False
    if not pd.isna(record['Telefono']):

        # Esperar a que el mensaje de error aparezca (max 5 segundos)
        try:
            error_message = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(text(),'ERROR:')]"))
            )
            # Si el mensaje de error está presente, hacer clic en el botón "Volver"
            time.sleep(1)
            volver_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
            )
            volver_button.click()
            hay_error = True
        except TimeoutException:
            pass
        try:
            # Esperar a que el mensaje de error aparezca (max 5 segundos)
            sirena_message = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[contains(., 'El simpatizante ya existe, fue registrado en info-sirena.')]"))
            )
            # Si el mensaje de error está presente, hacer clic en el botón "Volver"
            time.sleep(1)
            volver_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
            )
            volver_button.click()
            hay_error = True
        except TimeoutException:
            pass
        # Esperar a que el mensaje de error aparezca (max 5 segundos)
        try:
            error_message = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//b[contains(text(),'ERROR:')]"))
            )
            # Si el mensaje de error está presente, hacer clic en el botón "Volver"
            time.sleep(1)
            volver_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
            )
            volver_button.click()
            hay_error = True
        except TimeoutException:
            pass
    if not hay_error:
        # Seleccionar por direccion
        por_dir = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'apd'))
        )
        por_dir.click()

        # Cambiar a la nueva ventana o pestaña
        driver.switch_to.window(driver.window_handles[-1])

        # Esperar 5 segundos después de abrir la nueva página
        time.sleep(1)

        # Hacer clic en el botón "Actualizar coordenadas"
        actualizar_coordenadas_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'actualizar'))
        )
        actualizar_coordenadas_button.click()

        # Esperar a que el botón "Cerrar" sea clickeable
        time.sleep(1)
        cerrar_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btns.btns-gris[onclick='window.close();']"))
        )
        cerrar_button.click()

        driver.switch_to.window(driver.window_handles[-1])
        # Esperar a que el botón de promovidos sea clickeable y hacer clic
        time.sleep(1)
        volver_promovidos_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@onclick, 'window.location=\"./simpatiza.php\"')]"))
        )
        volver_promovidos_button.click()

        # Esperar a que el botón de registrar en línea sea clickeable y hacer clic
        registrar_en_linea_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btns.btns-ok span.ii i.fas.fa-link"))
        )
        registrar_en_linea_button.click()


def automate_web_form(user, password, records, chrome_driver_path, chrome_binary_path):
    driver = init_webdriver(chrome_driver_path, chrome_binary_path)

    try:
        login(driver, user, password)

        for record in records:
            fill_web_form(driver, record)
            # Agregar un tiempo de espera entre envíos si es necesario
            time.sleep(1)

    except TimeoutException as e:
        print(f"Se produjo un error con el mensaje: {e}")
    finally:
        driver.quit()

# Función principal que se llamará desde la UI


def main(usuario, contrasena, records, chrome_driver_path, chrome_binary_path):
    automate_web_form(usuario, contrasena, records,
                      chrome_driver_path, chrome_binary_path)


# Si vas a probar el script de forma independiente puedes usar esta parte,
# de lo contrario, estos datos vendrán de la UI
if __name__ == "__main__":
    usuario = 'tu_usuario'
    contrasena = 'tu_contraseña'
    # Esta lista debe contener diccionarios con los datos de cada registro válido
    records = [...]
    chrome_driver_path = 'env/chromedriver/chromedriver.exe'
    chrome_binary_path = 'env/chrome/chrome.exe'
    main(usuario, contrasena, records, chrome_driver_path, chrome_binary_path)
