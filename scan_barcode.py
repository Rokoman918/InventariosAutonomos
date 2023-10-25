# Importamos las librerías necesarias.
from argparse import ArgumentParser

import cv2
from pyzbar import pyzbar  # Esta es la librería que detectará y leerás los códigos de barra y QR

# Definimos el menú del programa.
argument_parser = ArgumentParser()
argument_parser.add_argument('-i', '--image', required=True, help='Ruta a la imagen de entrada.')
arguments = vars(argument_parser.parse_args())

# Leemos la imagen de entrada.
image = cv2.imread(arguments['image'])

# Extraemos los códigos de barra de la imagen.
barcodes = pyzbar.decode(image)

# Iteraremos por cada código de barra/QR hallado...
for i, barcode in enumerate(barcodes, start=1):
    # Extraemos el área del rectángulo que envuelve al código de barra, y lo pintamos en la imagen original.
    x, y, width, height = barcode.rect
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)

    # Decodificamos el tipo del código, así como la información que contiene.
    data = barcode.data.decode('utf-8')
    type_ = barcode.type

    # Imprimimos los datos del código de barras/QR
    print(f'Información del código de barra #{i}: {data}')
    print(f'Tipo del código de barra #{i}: {type_}')

    # Añadimos la una etiqueta con la información del código de barras/QR a la imagen.
    text = f'{data} ({type_})'
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

    # Guardamos el resultado en disco.
    # cv2.imwrite(f'result_{arguments["image"].rsplit("/")[1]}', image)
    cv2.imwrite(f'result_{arguments["image"].rsplit("/")[-1]}', image)
    # python scan_barcode.py -i barcodes3.jpg
