import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def procesar_pagina_simple(url):
    # Paso 1: Extraer el código fuente de la página
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Paso 2: Encontrar todas las etiquetas <img>
    imagenes = soup.find_all('img')

    # Paso 3: Descargar y procesar cada imagen
    for img in imagenes:
        try:
            img_url = img['src']
            if not img_url.startswith('http'):  # Si la URL es relativa, convertirla a absoluta
                img_url = os.path.join(url, img_url)

            respuesta_img = requests.get(img_url)
            imagen_binaria = BytesIO(respuesta_img.content)
            imagen = Image.open(imagen_binaria)

            # Paso 4: Redimensionar la imagen
            imagen.thumbnail((100, 100))

            # Paso 5: Guardar la imagen en un directorio
            if not os.path.exists('imagenes_descargadas'):
                os.makedirs('imagenes_descargadas')
            imagen.save(f'imagenes_descargadas/{os.path.basename(img_url)}')
        except Exception as e:
            print(f"Error al procesar la imagen {img_url}: {e}")