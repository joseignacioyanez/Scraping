from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

import json
import os

from os import listdir
from os.path import isfile, join

# For waits
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Merge PDFs
from PyPDF2 import PdfFileMerger

from pathlib import Path

##### Establecer Numero de MAteria y de Tema
numeroDeMateriaAScrapear = 4
numeroDeTemaAScrapear = 6

# Funciones

def mergePDFs():
    #Create and instance of PdfFileMerger() class
    merger = PdfFileMerger()
    #Create a list with PDF file names
    path_to_files = Path('PDF/')
    #Get the file names in the directory
    for root, dirs, file_names in os.walk(path_to_files):
        file_names.sort()
        #Iterate over the list of file names
        for file_name in file_names:
            if ".pdf" not in file_name:
                continue
            print("Imprimir")
            print(path_to_files)
            print(file_name)
            #Append PDF files
            pathNew = path_to_files / file_name
            pathNew = pathNew.resolve()
            merger.append(pathNew)
    #Write out the merged PDF
    archivo_unido = f"{materia}_{temaTitulo}_Completo.pdf"
    archivo_unido = archivo_unido.replace(":",".")
    merger.write(archivo_unido)
    merger.close()
    print("Merged Tema!")
    # Borrar Paginas individuales
    carpetaPDFs = Path("PDF/")
    onlyfiles = [f for f in listdir(carpetaPDFs) if isfile(join(carpetaPDFs, f))]
    for filePDF in onlyfiles:
        fileRemove = carpetaPDFs / filePDF
        os.remove(fileRemove)


def incrementarCounter():
    global counter
    counter = counter+1

def renombrarPdfImpreso(materia, temaTitulo, counter):
    # Cambiar nombre de hoja impresa
    nombre_antiguo = Path("PDF/Sistema Virtual de Educación [Contenidos].pdf")

    nombre_nuevo_base = Path("PDF/")

    numeroCounter = "XXX"
    #Agregar 0 a la izquierda 001
    if counter < 10:
        numeroCounter = f"00{counter}"
    elif counter < 100:
        numeroCounter = f"0{counter}"
    else:
        numeroCounter = counter

    nombre_nuevo_final = f"{materia}_{temaTitulo}_{numeroCounter}.pdf"
    
    nombre_nuevo_final = nombre_nuevo_final.replace(":",".")
    nombre_nuevo = nombre_nuevo_base / f"_{nombre_nuevo_final}"
    print(nombre_nuevo)
    print(counter)
    print("cintador en renombrarPDF")

    time.sleep(1)
    print("-> Nombre Antiguo")
    print(nombre_antiguo)
    print("-> Nombre Nuevo")
    print(nombre_nuevo)
    for i in range(30):
        for attempt in range(10):
            try:
                os.rename(nombre_antiguo, nombre_nuevo)
            except:
                continue
            else:
                break
        else:
            print("Se intento muchas veces y no se pudo renombrar los archivos")
    incrementarCounter()
    print(counter)
    print("cintador en renombrarPDF despues de sumar")

# TODO
def imprimirHTMLScrollable():
    # Lista para guardar los aria-labels
    aria_labels_Archive = []
    # Encontrar el texto 1ro (visible) y extraer aria-label e imprimir
    bloquesTexto = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'Text_Caption') and @class='cp-frameset']")
    for bloque in bloquesTexto:
        styleBloque = bloque.get_attribute("style")
        print("styleBloque-->" + styleBloque)
        # EEncontrar el alto del Text Caption para ver que no sea el titulo, mayor a 8%
        # TODO
        # Con JS calcular el alto y ver que sea mayor a +- 36px
        altoBloque = bloque.size['height']
        print("AltoBloque --> " + str(altoBloque))
        if altoBloque > 40 and "visibility: hidden" not in styleBloque:
            # Evitar que las Descripciones de Fifura salgan pero hay unos que la figura y el texto son unidos, ver que sea largo
            if bloque.get_attribute("aria-label").startswith("Figura") and len(bloque.get_attribute("aria-label")) < 400:
                continue
            aria_labels_Archive.append(bloque.get_attribute("aria-label"))
            print("Debug")
            print(bloque.get_attribute("aria-label"))
    
    newAriaLabel = ""
    # Mientras no tenga el aria label en la lista, imprimir
    while newAriaLabel != aria_labels_Archive[0]:
        # Encontrar el Boton Down y presionar
        driver.find_element(By.XPATH, "//div[starts-with(@id,'pgdn_') and @class='cp-frameset']").click()
        # Buscar el texto vsible y aniadirlo al array. 
        for bloque in bloquesTexto:
            styleBloque = bloque.get_attribute("style")
            altoBloque = bloque.size['height']
            if altoBloque > 40 and "visibility: hidden" not in styleBloque:
                aria_labels_Archive.append(bloque.get_attribute("aria-label"))
                newAriaLabel = bloque.get_attribute("aria-label")
        
        print("newAriaLabel--->")
        print(newAriaLabel)
        print("Archive-->")
        print(aria_labels_Archive)
        # imprimir
        driver.execute_script('window.print();')
        time.sleep(2)
        renombrarPdfImpreso(materia, temaTitulo, counter)


def entrarEnIframe(iframeSecundario):
    # cambiar iframe driver
    driver.switch_to.frame(iframeSecundario)
    # Imprimir
    driver.execute_script('window.print();')
    # renombrar el que se imprimio
    renombrarPdfImpreso(materia, temaTitulo, counter)
    return

def enPaginaFinal():
    results = driver.find_elements(By.XPATH, "//div[@aria-label='Review Quiz ']")
    if not results:
        return False
    else:
        return True
def enPreguntaFinal():
    results = driver.find_elements(By.XPATH, "//div[@aria-label='Pregunta 10 de 10    ']")
    if not results:
        return False
    else:
        return True

# Para saber si existen iframes con texto dentro del iframe prncipal
def hayIframes():
    # Identificar si hay un iframe dentro de la pagina
    iframesInternos = driver.find_elements(By.TAG_NAME, "iframe")
    if iframesInternos:
        return True
    else:
        return False
    
# Para saber si exsten cuadros tde texto dentro con HTML Scrollable
def hayHTMLScrollable():
    htmlsScrollables = driver.find_elements(By.XPATH, "//div[starts-with(@id,'pgdn_') and @class='cp-frameset']")
    if htmlsScrollables:
        return True
    else:
        return False

def imprimirTema(tema):
    # Hacer click en el tema en la de contenidos
    for i in range(30):
        for attempt in range(10):
            try:
                tema.click()
            except:
                continue
            else:
                break
        else:
            print("Se intento muchas veces y no se pudo hacer click en el tema")

    ## Ingresar a cada tema
    time.sleep(5)

    ## TODO
    ## Hacer que esto solo pase si ya he hecho la autoevaluacion
    ## Abrir tema si no se abre automaticamente
    # driver.find_element(By.XPATH, "//ul[@class='main_branch']/li/div").click()

    #time.sleep(5)

    # Cambio al iframe 
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # Imagen Play iniciar tema
    time.sleep(8)
    driver.find_element(By.ID, "playImage").click()
    
    # Si se resume en media unidad, abrir menu e ir a titulo
    time.sleep(2)
    for i in range(30):
        for attempt in range(10):
            try:
                driver.find_element(By.ID, "expandIcon").click()
            except:
                continue
            else:
                break
        else:
            print("Se intento muchas veces y no se pudo hacer click en el menu expand")
    for i in range(5):
        for attempt in range(10):
            try:
                driver.find_element(By.XPATH, "//div[@id='tocContent']/div[@class='tocEntryContainerStyle']").click()
            except:
                continue
            else:
                break
        else:
            print("Se intento muchas veces y no se pudo hacer click en el Encabezado")
    
    # Necesrio en Mac en la Portada
    for i in range(30):
        for attempt in range(10):
            try:
                driver.find_element(By.ID, "collapseIcon").click()    
            except:
                continue
            else:
                break
        else:
            print("Se intento muchas veces y no se pudo hacer click en cerrar el menu")

    time.sleep(2)

    # Guardar Cabecera
    # 1. Imprimir con Navegado
    while not enPreguntaFinal():
        # Imprime
        print(counter)
        print("cintador en main")
        driver.execute_script('window.print();')
        time.sleep(2)
        renombrarPdfImpreso(materia, temaTitulo, counter)

        # Identificar si hay un iframe dentro de la pagina
        if hayIframes():
            # Entrar en el iframe e imprimir
            # usar funcion nueva
            print("Hay iframe interno")
            iframesInternos = driver.find_elements(By.TAG_NAME, "iframe")
            entrarEnIframe(iframesInternos[0])
            # Cambiar al iframe primario 
            # regresando al default antes para poder ir a sgte pagina
            driver.switch_to.default_content()
            # cambiar iframe driver
            iframePrimario = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframePrimario)
            # Click en la siguiente pagina
            driver.find_element(By.XPATH, "//div[starts-with(@id, 'eLB_skin01_next') and @class='cp-frameset']").click()
        elif hayHTMLScrollable():
            print("Hay HTML Scrollable")
            imprimirHTMLScrollable()
            # Click en la siguiente pagina
            driver.find_element(By.XPATH, "//div[starts-with(@id, 'eLB_skin01_next') and @class='cp-frameset']").click()
        else:
            print("No hya nada, prosigo")
            # Aumenta contador
            # Click en la siguiente pagina
            driver.find_element(By.XPATH, "//div[starts-with(@id, 'eLB_skin01_next') and @class='cp-frameset']").click()
            
        time.sleep(2)

    # Merge PDFs
    mergePDFs()
    # Salir al frame principal y hacer clicck en boton de cerrar frame
    driver.switch_to.default_content()
    driver.find_elements(By.XPATH, "//button[@class='zoom_in zoom_button']")[1].click()
    # Salir a Contenidos
    driver.find_elements(By.XPATH, "//div[@class='breadcrumb']/a")[0].click()
    print("Sali a Contenidos")


# Settings para Imprimir
print_settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": "",
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False,
    "isLandscapeEnabled": True
}
# No se ocmo hacer en Mac y Windows

prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(print_settings),
    "download.prompt_for_download": False,
    "profile.default_content_setting_values.automatic_download": 1,
    "download.default_directory": "/Users/joseignacio/Desktop/vacaciones laptop/Scraping/PDF/",
    "savefile.default_directory": "/Users/joseignacio/Desktop/vacaciones laptop/Scraping/PDF/",
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
# Abrir Navegador
options= Options()
options.add_experimental_option('prefs', prefs)
options.add_argument('--kiosk-printing')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
# De aqui arriba elimine esto: , options=options comoa tributo
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1080)

# Ingresar en MiESPE

driver.get("http://miespe.espe.edu.ec/")

assert "ESPE" in driver.title

usernameESPE = driver.find_element(By.ID, "username")
usernameESPE.clear()
usernameESPE.send_keys("jiyanez1")

passwordESPE = driver.find_element(By.ID, "password")
passwordESPE.clear()
passwordESPE.send_keys("030999")

usernameESPE.send_keys(Keys.RETURN)

# Setup wait for later
wait = WebDriverWait(driver, 10)
# Store the ID of the original window
original_window = driver.current_window_handle
# Check we don't have other windows open already
assert len(driver.window_handles) == 1

# Entrar a Educativa
driver.find_element(By.LINK_TEXT, "Modalidad en Línea").click()

# Wait for the new window or tab
wait.until(EC.number_of_windows_to_be(2))

# Loop through until we find a new window handle
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break

# Wait for the new tab to finish loading content
wait.until(EC.title_is("Sistema Virtual de Educación [Inicio]"))

print(driver.title)
assert "Inicio" in driver.title


## Escoger materia
resultSet  = driver.find_element(By.XPATH, "//ul[@class='lista_aulas']")
clases = resultSet.find_elements(By.TAG_NAME, "li")

'''
for clase in clases:
Si se quiere que haga todas las materias, indentar todo lo de abajo'''    
clase = clases[numeroDeMateriaAScrapear]
for i in range(30):
    for attempt in range(10):
        try:
            linkClase = clase.find_element(By.XPATH, ".//article/header/a")
            linkClase.click()
        except:
            continue
        else:
            break
    else:
        print("Se intento muchas veces y no se pudo hacer click en la materia")

time.sleep(2)

# Extraer Materia
materia = driver.find_element(By.XPATH, "//h1[@class='corte_palabras']").text

contenidosLink = driver.find_element(By.LINK_TEXT, "Contenidos")
contenidosLink.click()

time.sleep(1)

bloqueUnidades = driver.find_element(By.XPATH, "//ul[@class='unidades']")
unidades = bloqueUnidades.find_elements(By.XPATH, "./*")

for unidad in unidades:
    if 'show' not in unidad.get_attribute("class"):
        unidad.find_element(By.XPATH, ".//h3").click()

temas = driver.find_elements(By.XPATH, "//a[@class='item_nombre linea_unica']")
'''
for tema in temas:
Si se quiere que analice todos los temas, indentar lo de abajo
'''
tema = temas[numeroDeTemaAScrapear]
# Extraer tema
temaTitulo = tema.text

counter = 0

imprimirTema(tema)

# Volver a Inicio
driver.find_element(By.XPATH, "//a[@class='logo']/img").click()
print("Sali al Inicio")
    
'''
# Salir al frame principal y hacer clicck en boton de cerrar frame
driver.switch_to.default_content()
driver.find_elements(By.XPATH, "//button[@class='zoom_in zoom_button']")[1].click()
'''
    