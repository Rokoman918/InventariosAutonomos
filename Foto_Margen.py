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

# Función para detectar etiquetas con líneas similares a código de barras
def detectar_etiqueta(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización para resaltar las líneas similares a código de barras
    _, etiqueta_umbralizada = cv2.threshold(imagen_gris, 100, 255, cv2.THRESH_BINARY)

    # Encontrar los contornos en la imagen umbralizada
    contornos, _ = cv2.findContours(etiqueta_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar el contorno más grande
    contorno_mas_grande = max(contornos, key=cv2.contourArea)

    # Obtener las coordenadas del rectángulo delimitador de la etiqueta
    x, y, w, h = cv2.boundingRect(contorno_mas_grande)

    # Agregar un margen de 2 centímetros
    margen = 20  # 20 píxeles es un margen de aproximadamente 2 centímetros en una imagen típica
    x -= margen
    y -= margen
    w += 2 * margen
    h += 2 * margen

    # Recortar la etiqueta de la imagen original
    etiqueta_recortada = imagen[y:y+h, x:x+w]

    return etiqueta_recortada, x, y, w, h

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

    # Detección de etiqueta con líneas similares a código de barras
    etiqueta, x, y, w, h = detectar_etiqueta(imagen)

    if etiqueta is not None and w > 0 and h > 0:
        # Dibuja un rectángulo rojo alrededor del código de barras con un margen de 1 centímetro
        margen_rojo = 10  # 10 píxeles es un margen de aproximadamente 1 centímetro
        cv2.rectangle(imagen, (x - margen_rojo, y - margen_rojo), (x + w + margen_rojo, y + h + margen_rojo), (0, 0, 255), 2)

        # Detección de códigos de barras
        codigo_barras = decode(etiqueta)
        if codigo_barras:
            # Obtiene el valor del código de barras
            codigo = codigo_barras[0].data.decode("utf-8")

            # Dibuja el número del código de barras en la imagen
            cv2.putText(imagen, codigo, (x - margen_rojo, y - margen_rojo - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            print(f"Código de barras detectado: {codigo}")

            # Guarda la imagen de la etiqueta con el rectángulo y el código superpuesto
            cv2.imwrite(imagen_etiqueta_path, imagen)

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

