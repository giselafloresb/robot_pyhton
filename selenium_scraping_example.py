# Librerías
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import sys 
import time
from openpyxl import load_workbook

#ruta del ejecutable de ChromeDriver
driver_path = 'C:\\Users\\gisel\\Desktop\\chromedriver-win64\\chromedriver.exe'

# Ruta del archivo Excel
excel_path = 'C:\\Users\\gisel\\Documents\\robot_pyhton\\CAPTURA VIERNES 08 DIC.xlsx'

# Opciones del navegación
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

#Iniciar el navegador
options.binary_location = 'C:\\Users\\gisel\\Desktop\\chrome-win64\\chrome.exe'
driver = webdriver.Chrome(options=options)

# Iniciar el navegador en una posición determinada
try:
    # Ingresar a la página
    driver.get('https://info.sirena.mx/index.php')

    # Esperar hasta que el elemento sea clickeable
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='login']"))
    )
    username.send_keys('bezaadttvy')

    password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    password.send_keys('MQ8kpmbrgj')

    driver.find_element('id', 'go').click()

    # Seleccionar botones
    promovidos_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'window.location=\"./simpatiza.php\"')]"))
    )
    promovidos_button.click()

    registrar_en_linea_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btns.btns-ok span.ii i.fas.fa-link"))
    )
    registrar_en_linea_button.click()

    # Cambiar a la nueva ventana o pestaña (si es necesario)
    driver.switch_to.window(driver.window_handles[-1])

    # Esperar hasta que el radio button sea clickeable
    simpatizante_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'xxsimpatizante1'))
    )
    simpatizante_radio_button.click()

    # Verificar si es simpatizante
    if simpatizante_radio_button: 

        workbook = load_workbook(excel_path)
        sheet = workbook.active  

        # Obtener datos del Excel
        nombre = sheet['A2'].value
        apellidop = sheet['B2'].value
        apellidom = sheet['C2'].value
        #cve_ife = sheet[].value
        calle = sheet['D2'].value
        ext = sheet['E2'].value  
        municipio = sheet['F2'].value
        colonia = sheet['G2'].value
        seccion = sheet['H2'].value
        telefono = sheet['I2'].value

        # Seleccionar la opción para "medad"
        medad_option = driver.find_element(By.ID, 'xxmedad1')
        medad_option.click()

        # Ingresar información en los campos
        nombre_input = driver.find_element(By.ID, 'nombre')
        nombre_input.send_keys(nombre)
        
        time.sleep(1)
        apellidop_input = driver.find_element(By.ID, 'paterno')
        apellidop_input.send_keys(apellidop)

        time.sleep(1)
        apellidom_input = driver.find_element(By.ID, 'materno')
        apellidom_input.send_keys(apellidom)

        time.sleep(1)
        calle_input = driver.find_element(By.ID, 'calle')
        calle_input.send_keys(calle)

        time.sleep(1)
        ext_input = driver.find_element(By.ID, 'num_ext')
        ext_input.send_keys(ext)

        time.sleep(1)
        municipio_dropdown = driver.find_element(By.ID, 'municipio')
        municipio_dropdown.send_keys(municipio)

        time.sleep(1)
        colonia_input = driver.find_element(By.ID, 'colonia')
        colonia_input.send_keys(colonia)

        time.sleep(1)
        seccion_dropdown = driver.find_element(By.ID, 'seccion')
        seccion_dropdown.send_keys(seccion)

        # Verificar si el valor ingresado está presente en el campo
        # try:
        #     # Esperar hasta que el elemento con el valor ingresado aparezca
        #     WebDriverWait(driver, 2).until(
        #         EC.text_to_be_present_in_element((By.XPATH, '//*[@id="seccion"]'), seccion)
        #     )

            # Si encuentra el valor, seguir con el resto del código...
        tel_input = driver.find_element(By.ID, 'tel')
        tel_input.send_keys(telefono)

            # Hacer clic en cualquier parte de la página
        driver.find_element('id','info').click()

        # Hacer clic en el botón "Enviar/Guardar"
        enviar_guardar_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.ID, 'submitokm'))
        )
        enviar_guardar_button.click()

        # Esperar a que el mensaje de error aparezca (max 5 segundos)
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'ERROR:')]"))
        )

        # Si el mensaje de error está presente, hacer clic en el botón "Volver"
        volver_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'window.location=\"./sload.php\"')]"))
        )
        volver_button.click()

        #Seleccionar por direccion
        por_dir = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'apd'))
        )
        por_dir.click()

        # Cambiar a la nueva ventana o pestaña
        driver.switch_to.window(driver.window_handles[-1])

        # Esperar 5 segundos después de abrir la nueva página
        time.sleep(5)

        # Hacer clic en el botón "Actualizar coordenadas"
        actualizar_coordenadas_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'actualizar'))
        )
        actualizar_coordenadas_button.click()

        # Esperar a que el botón "Cerrar" sea clickeable
        time.sleep(2)
        cerrar_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btns.btns-gris[onclick='window.close();']"))
        )
        cerrar_button.click()

        # except TimeoutException:
        #     # Si el valor no está presente, hacer clic en el botón "Volver"
        #     volver_button = WebDriverWait(driver, 2).until(
        #         EC.element_to_be_clickable((By.XPATH, '//*[@id="msgs"]/p[2]/button'))
        #     )
        #     volver_button.click()

# No se encontró el mensaje de error, continuar con el resto del código
except TimeoutException:
    pass

finally:
    time.sleep(50)
    driver.quit()
