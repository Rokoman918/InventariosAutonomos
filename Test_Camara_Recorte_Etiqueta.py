import cv2
import os
import subprocess
from pyzbar.pyzbar import decode

# Función para capturar una imagen desde la cámara
def capturar_imagen(camara, ruta_destino):
    ret, imagen = camara.read()
    if ret:
        cv2.imwrite(ruta_destino, imagen)
        cv2.imshow("Cámara", imagen)  # Muestra la imagen en pantalla

# Función para detectar etiquetas con fondo blanco
def detectar_etiqueta(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización para detectar el fondo blanco
    _, etiqueta_umbralizada = cv2.threshold(imagen_gris, 200, 255, cv2.THRESH_BINARY)

    # Encontrar los contornos en la imagen umbralizada
    contornos, _ = cv2.findContours(etiqueta_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar el contorno más grande
    contorno_mas_grande = max(contornos, key=cv2.contourArea)

    # Obtener las coordenadas del rectángulo delimitador de la etiqueta
    x, y, w, h = cv2.boundingRect(contorno_mas_grande)

    # Recortar la etiqueta de la imagen original
    etiqueta_recortada = imagen[y:y+h, x:x+w]

    return etiqueta_recortada

# Ruta de la cámara
camara = cv2.VideoCapture(0)

# Ruta de la imagen de salida
imagen_cama_path = "imagen_cama.jpg"

# Ruta de la imagen de etiqueta
imagen_etiqueta_path = "imagen_etiqueta.jpg"

# Crea una ventana para mostrar la imagen de la cámara
cv2.namedWindow("Cámara", cv2.WINDOW_NORMAL)

while True:
    # Captura una imagen desde la cámara
    capturar_imagen(camara, imagen_cama_path)

    # Cargar la imagen capturada
    imagen = cv2.imread(imagen_cama_path)

    # Detección de etiqueta con fondo blanco
    etiqueta = detectar_etiqueta(imagen)

    if etiqueta is not None:
        # Guarda la imagen de la etiqueta
        cv2.imwrite(imagen_etiqueta_path, etiqueta)

        # Ejecutar el análisis de extracción de texto usando extraeTexto.py
        comando_analisis_texto = f"python extraeTexto.py -i {imagen_etiqueta_path}"
        subprocess.run(comando_analisis_texto, shell=True)

    # Espera una tecla para continuar o presiona 'q' para salir
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break

# Libera la cámara, cierra las ventanas y destruye la ventana "Cámara"
camara.release()
cv2.destroyAllWindows()
cv2.destroyWindow("Cámara")
