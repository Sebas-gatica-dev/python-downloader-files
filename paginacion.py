import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def procesar_paginacion(url_base):
    page = 1
    while True:
        url = f"{url_base}?page={page}"  # Ajusta el formato de la URL según la página
        respuesta = requests.get(url)
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        # Buscar las imágenes en la página actual
        imagenes = soup.find_all('img')
        if not imagenes:  # Si no hay más imágenes, terminar
            break

        for img in imagenes:
            try:
                img_url = img['src']
                if not img_url.startswith('http'):  # Si la URL es relativa, convertirla a absoluta
                    img_url = os.path.join(url_base, img_url)

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

        page += 1  # Pasar a la siguiente página