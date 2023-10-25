#Este codigo busca detectar una etiqueta en una foto de una caja para recortarla y eliminar ruido para extracción de datos 
from argparse import ArgumentParser
from PIL import Image
import cv2
import os
import subprocess

# Definimos el menú del programa.
argument_parser = ArgumentParser()
argument_parser.add_argument('-i', '--image', required=True, help='Ruta a la imagen de entrada.')

arguments = vars(argument_parser.parse_args())

# Leemos la imagen de entrada.
ruta_imagen = arguments['image']

# Ruta de la imagen de la que deseas extraer texto
#imagen = Image.open(ruta_imagen)

# Cargar la imagen
imagen = cv2.imread(ruta_imagen)

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar umbralización para detectar la etiqueta blanca
_, etiqueta_umbralizada = cv2.threshold(imagen_gris, 200, 255, cv2.THRESH_BINARY)

# Encontrar los contornos en la imagen umbralizada
contornos, _ = cv2.findContours(etiqueta_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Encontrar el contorno más grande, que probablemente sea la etiqueta
contorno_mas_grande = max(contornos, key=cv2.contourArea)

# Obtener las coordenadas del rectángulo delimitador de la etiqueta
x, y, w, h = cv2.boundingRect(contorno_mas_grande)

# Recortar la etiqueta de la imagen original
etiqueta_recortada = imagen[y:y+h, x:x+w]

# Guardar o mostrar la etiqueta recortada
cv2.imwrite("etiqueta_recortada.jpg", etiqueta_recortada)
cv2.imshow("Etiqueta Recortada", etiqueta_recortada)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Crear una carpeta "Etiquetas_Procesadas" si no existe
carpeta_salida = "Etiquetas_Procesadas"
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Guardar la etiqueta recortada en la carpeta "Etiquetas_Procesadas"
etiqueta_recortada_path = os.path.join(carpeta_salida, "etiqueta_recortada.jpg")
cv2.imwrite(etiqueta_recortada_path, etiqueta_recortada)

# Ejecutar el análisis de extracción de texto usando extraeTexto.py
comando_analisis_texto = f"python extraeTexto.py -i {etiqueta_recortada_path}"
subprocess.run(comando_analisis_texto, shell=True)