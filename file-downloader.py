import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Paso 1: extraer el condigo fuente de la página
url = 'https://es.pinterest.com/demorros20/im%C3%A1genes-gratuitas/'
respuesta = requests.get(url)
soup = BeautifulSoup(respuesta.text, 'html.parser')

# Paso 2: Encontrar todas las etiquetas <img> de es apagina web
imagenes = soup.find_all('img')

# Paso 3: Descargar y procesar cada imagen
for img in imagenes:
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