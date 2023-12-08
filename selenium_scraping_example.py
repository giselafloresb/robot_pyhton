# Librerías
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

#ruta del ejecutable de ChromeDriver
driver_path = 'C:\\Users\\gisel\\Desktop\\chromedriver-win64\\chromedriver.exe'

# Opciones del navegación
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
#options.add_argument('--disable-extensions')

#Iniciar el navegador
options.binary_location = 'C:\\Users\\gisel\\Desktop\\chrome-win64\\chrome.exe'

# Aquí se corrige la forma en que se pasan las opciones al WebDriver
driver = webdriver.Chrome(options=options)

# Leer datos desde el archivo Excel
#excel_path = 'C:\\Users\\gisel\\Documents\\robot_pyhton\\CAPTURA MIERCOLES 06 DIC.xlsx'
#df = pd.read_excel(excel_path)

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

        # Seleccionar la opción para "medad"
        medad_option = driver.find_element(By.CSS_SELECTOR, "input[name='medad']")
        medad_option.click()

        # Ingresar información en los campos
        nombre_input = driver.find_element(By.ID, 'nombre')
        nombre_input.send_keys('ANTONIO')
        
        time.sleep(1)
        apellidop_input = driver.find_element(By.ID, 'paterno')
        apellidop_input.send_keys('LOPEZ')

        time.sleep(1)
        apellidom_input = driver.find_element(By.ID, 'materno')
        apellidom_input.send_keys('REINA')

        time.sleep(1)
        calle_input = driver.find_element(By.ID, 'calle')
        calle_input.send_keys('AVENIDA VERDUGO')

        time.sleep(1)
        ext_input = driver.find_element(By.ID, 'num_ext')
        ext_input.send_keys('47')

        time.sleep(1)
        municipio_dropdown = driver.find_element(By.ID, 'municipio')
        municipio_dropdown.send_keys('Mexicali')

        time.sleep(1)
        colonia_input = driver.find_element(By.ID, 'colonia')
        colonia_input.send_keys('CIUDAD COAHUILA')

        time.sleep(1)
        seccion_dropdown = driver.find_element(By.ID, 'seccion')
        seccion_dropdown.send_keys('644')

        time.sleep(1)
        tel_input = driver.find_element(By.ID, 'tel')
        tel_input.send_keys('6861993643')
        
        # Hacer clic en cualquier parte de la página
        driver.find_element('id','info').click()

        # Hacer clic en el botón "Enviar/Guardar"
        enviar_guardar_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.ID, 'submitokm'))
        )
        enviar_guardar_button.click()

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


    else:
        # Ingresar información si no es simpatizante
        driver.find_element('input[name="calle"]').send_keys('NombreCalle')
        driver.find_element('input[name="num_ext"]').send_keys('NumeroExterior')
        driver.find_element('input[name="municipio"]').send_keys('Mexicali')
        driver.find_element('input[name="colonia"]').send_keys('NombreColonia')
        driver.find_element('input[name="seccion"]').send_keys('Seccion')

        # Hacer clic en cualquier parte de la página (puedes cambiar el selector según tu necesidad)
        driver.find_element('body').click()

        # Seleccionar botones adicionales
        driver.find_element('input[name="button"][id="submitokm"]').click()
        driver.find_element('input[name="buton"][id="apd"]').click()

        # Abrir nueva pestaña
        driver.execute_script("window.open('https://2024.sirena.mx/upcoor.php', '_blank')")

        # Esperar 3 segundos
        time.sleep(3)

        # Actualizar y cerrar la nueva pestaña
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element('input[name="button"][id="actualizar"]').click()
        time.sleep(1)
        driver.find_element('input[name="button"][id="window.close()"]').click()

finally:
    time.sleep(50)
    driver.quit()
