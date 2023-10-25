import cv2
import os
import subprocess
from pyzbar.pyzbar import decode

# Función para capturar una imagen desde la cámara
def capturar_imagen(camara, ruta_destino):
    ret, imagen = camara.read()
    if ret:
        cv2.imwrite(ruta_destino, imagen)

# Ruta de la cámara
camara = cv2.VideoCapture(0)


# Crear una carpeta "Etiquetas_Procesadas" si no existe
carpeta_salida = "Camara"
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)


# Ruta de la imagen de salida
imagen_cama_path = os.path.join(carpeta_salida, "/imagen_cama.jpg")

# Ruta de la imagen de etiqueta
imagen_etiqueta_path = "images/Etiquetas/imagen_etiqueta.jpg"


# Crea una ventana para mostrar la imagen de la cámara
cv2.namedWindow("Cámara", cv2.WINDOW_NORMAL)



# Detección de códigos de barras
def detectar_codigo_de_barras(imagen):
    codigo_barras_decodificados = decode(imagen)
    for codigo_barras_decodificado in codigo_barras_decodificados:
        return codigo_barras_decodificado.data.decode("utf-8")
    return None

while True:
    # Captura una imagen desde la cámara
    capturar_imagen(camara, imagen_cama_path)

    # Cargar la imagen capturada
    imagen = cv2.imread(imagen_cama_path)

    # Detección de códigos de barras
    codigo_barras = detectar_codigo_de_barras(imagen)

    if codigo_barras:
        print(f"Código de barras detectado: {codigo_barras}")

        # Guarda la imagen de la cama
        cv2.imwrite(imagen_etiqueta_path, imagen)

        # Ejecutar el análisis de extracción de texto usando extraeTexto.py
        comando_analisis_texto = f"python extraeTexto.py -i {imagen_etiqueta_path}"
        subprocess.run(comando_analisis_texto, shell=True)

    # Espera una tecla para continuar o presiona 'q' para salir
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break

# Libera la cámara y cierra las ventanas
camara.release()
cv2.destroyAllWindows()
