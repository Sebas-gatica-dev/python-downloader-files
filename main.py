import os
import requests
from bs4 import BeautifulSoup

# Importar los módulos específicos
from sin_carga_especial import procesar_pagina_simple
from paginacion import procesar_paginacion
from infinite_scroll import procesar_infinite_scroll

def detectar_tipo_carga(url):
    """
    Detecta si la página usa paginación, infinite scroll o ninguna de las dos.
    """
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Verificar si hay paginación
    paginacion = soup.find_all('a', {'class': 'pagination-link'})  # Ajusta el selector según la página
    if paginacion:
        return "paginacion"

    # Verificar si hay infinite scroll (inspeccionando scripts o patrones comunes)
    scripts = soup.find_all('script')
    for script in scripts:
        if "infinite-scroll" in str(script) or "load-more" in str(script):
            return "infinite_scroll"

    # Si no se detecta ninguno, asumimos que no hay paginación ni infinite scroll
    return "sin_carga_especial"


if __name__ == "__main__":
    url = 'https://es.pinterest.com/demorros20/imágenes-gratuitas/'
    tipo_carga = detectar_tipo_carga(url)

    if tipo_carga == "paginacion":
        print("La página usa paginación.")
        procesar_paginacion(url)
    elif tipo_carga == "infinite_scroll":
        print("La página usa infinite scroll.")
        procesar_infinite_scroll(url)
    else:
        print("La página no usa paginación ni infinite scroll.")
        procesar_pagina_simple(url)