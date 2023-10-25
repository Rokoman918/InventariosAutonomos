#Este codigo esta uniendo dos modulos para procesarlos


import cv2
from pyzbar.pyzbar import decode

# Función para cargar una imagen desde la ruta
def cargar_imagen(ruta):
    return cv2.imread(ruta)

# Función para detectar códigos de barras en una imagen
def detectar_codigos(image):
    return decode(image)

# Función para recortar y guardar un código de barras
def recortar_y_guardar_codigo(image, codigo, nombre_archivo):
    if codigo:
        codigo = codigo[0]  # Tomamos el primer código de barras detectado
        x, y, w, h = codigo.rect
        barcode_image = image[y:y + h, x:x + w]
        cv2.imwrite(nombre_archivo, barcode_image)
        print(f'Código de barras recortado y guardado como {nombre_archivo}')
    else:
        print('No se encontraron códigos de barras en la imagen')

# Rutas de las imágenes
imagen_1 = 'D:/Labs/Jetson/inference/training/detection/cb(1).jpeg'
imagen_2 = 'D:/Labs/Jetson/inference/training/detection/cb(2).jpeg'

# Cargamos la primera imagen
image1 = cargar_imagen(imagen_1)

# Detectamos códigos de barras en la primera imagen
codigos1 = detectar_codigos(image1)

# Recortamos y guardamos el código de barras de la primera imagen
recortar_y_guardar_codigo(image1, codigos1, 'codigo_recortado_1.jpg')

# Cargamos la segunda imagen
image2 = cargar_imagen(imagen_2)

# Detectamos códigos de barras en la segunda imagen
codigos2 = detectar_codigos(image2)

# Recortamos y guardamos el código de barras de la segunda imagen
recortar_y_guardar_codigo(image2, codigos2, 'codigo_recortado_2.jpg')