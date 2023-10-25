
from argparse import ArgumentParser
import pytesseract
from PIL import Image


# Definimos el menú del programa.
argument_parser = ArgumentParser()
argument_parser.add_argument('-i', '--image', required=True, help='Ruta a la imagen de entrada.')
arguments = vars(argument_parser.parse_args())

# Leemos la imagen de entrada.
ruta_imagen = arguments['image']

# Ruta de la imagen de la que deseas extraer texto
#ruta_imagen = 'D:/Labs/Jetson/inference/training/detection/cb(1)r.jpg'

# Cargar la imagen usando la biblioteca Pillow (PIL)
imagen = Image.open(ruta_imagen)

# Utilizar Tesseract OCR para extraer el texto
texto_extraido = pytesseract.image_to_string(imagen)

# Imprimir el texto extraído
print(texto_extraido)