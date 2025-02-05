import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def procesar_infinite_scroll(url):
    # Configurar Selenium con un navegador (por ejemplo, Chrome)
    driver = webdriver.Chrome()

    # Abrir la página
    driver.get(url)

    # Simular scroll hacia abajo
    scrolls = 5  # Número de veces que quieres hacer scroll
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Esperar a que se cargue el nuevo contenido

    # Obtener el HTML después de cargar todo el contenido
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrar todas las etiquetas <img>
    imagenes = soup.find_all('img')

    # Descargar y procesar cada imagen
    for img in imagenes:
        try:
            img_url = img['src']
            if not img_url.startswith('http'):  # Si la URL es relativa, convertirla a absoluta
                img_url = os.path.join(url, img_url)

            respuesta_img = requests.get(img_url)
            imagen_binaria = BytesIO(respuesta_img.content)
            imagen = Image.open(imagen_binaria)

            # Redimensionar la imagen
            imagen.thumbnail((100, 100))

            # Guardar la imagen en un directorio
            if not os.path.exists('imagenes_descargadas'):
                os.makedirs('imagenes_descargadas')
            imagen.save(f'imagenes_descargadas/{os.path.basename(img_url)}')
        except Exception as e:
            print(f"Error al procesar la imagen {img_url}: {e}")

    # Cerrar el navegador
    driver.quit()