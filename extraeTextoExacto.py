from argparse import ArgumentParser
import pytesseract
from PIL import Image
import re

# Definimos el menú del programa.
argument_parser = ArgumentParser()
argument_parser.add_argument('-i', '--image', required=True, help='Ruta a la imagen de entrada.')
argument_parser.add_argument('-w', '--word', required=True, help='Palabra clave a buscar.')
arguments = vars(argument_parser.parse_args())

# Leemos la imagen de entrada.
ruta_imagen = arguments['image']

# Ruta de la imagen de la que deseas extraer texto
imagen = Image.open(ruta_imagen)

# Utilizar Tesseract OCR para extraer el texto
texto_extraido = pytesseract.image_to_string(imagen)

#print(texto_extraido)

# Buscar la palabra clave en el texto
palabra_clave = arguments['word']


# Buscar 10 caracteres después de la palabra clave
# patron = re.compile(fr'{re.escape(palabra_clave)}\s*(.*)', re.DOTALL)  # Agregar re.DOTALL para manejar saltos de línea

#resultado = patron.search(texto_extraido)

#if resultado:
#    caracteres = resultado.group(1)  # Obtiene los 10 caracteres
#    print(f'Caracteres encontrados: {caracteres}')
#else:
#    print(f'Palabra clave "{palabra_clave}" no encontrada o sin 10 caracteres siguientes.')


found = texto_extraido.find(palabra_clave)
tamaño_palabra_clave = len(palabra_clave)

#if found != -1:
#    resultado = texto_extraido[found + 10:]
#    print(f'Caracteres encontrados: {resultado}')
#else:
#    print(f'Palabra clave "{palabra_clave}" no encontrada o sin 10 caracteres siguientes.')

print(found)

if found != -1:
    end_index = texto_extraido.find("\n", found)
    if end_index != -1:
        resultado = texto_extraido[found + tamaño_palabra_clave  :end_index]
    else:
        resultado = texto_extraido[found + tamaño_palabra_clave :]
    print(f'Caracteres encontrados para : {resultado}')
else:
    print(f'Palabra clave "{palabra_clave}" no encontrada o sin 10 caracteres siguientes.')
