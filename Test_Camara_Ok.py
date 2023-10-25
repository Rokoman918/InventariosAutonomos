import cv2
import csv
import os
import subprocess
from pyzbar.pyzbar import decode

# Función para capturar una imagen desde la cámara
def capturar_imagen(camara, ruta_destino):
    ret, imagen = camara.read()
    if ret:
        cv2.imwrite(ruta_destino, imagen)
        cv2.imshow("Cámara", imagen)  # Muestra la imagen en pantalla

# Ruta de archivo CSV
archivo_csv_path = "datos/archivo_csv/resultados_codigos_barras.csv"

# Ruta de la cámara
camara = cv2.VideoCapture(0)

# Ruta de la imagen de salida
imagen_cama_path = "imagen_cama.jpg"

# Ruta de la imagen de etiqueta
imagen_etiqueta_path = "imagen_etiqueta.jpg"

# Crea una ventana para mostrar la imagen de la cámara
cv2.namedWindow("Cámara", cv2.WINDOW_NORMAL)

# Detección de códigos de barras
def detectar_codigo_de_barras(imagen):
    codigo_barras_decodificados = decode(imagen)
    for codigo_barras_decodificado in codigo_barras_decodificados:
        return codigo_barras_decodificado.data.decode("utf-8")
    return None

# Crea encabezado del archivo
with open(archivo_csv_path, mode='w', newline='') as archivo_csv:
    campos = ['Codigo de Barras', 'Ubicacion']
    escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

    escritor_csv.writeheader()

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
        
        # Abre el archivo CSV en modo 'append' para agregar nuevas filas
        with open(archivo_csv_path, mode='a', newline='') as archivo_csv:
            campos = ['Codigo de Barras', 'Ubicacion']
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

            # Guarda el resultado en el archivo CSV
            escritor_csv.writerow({'Codigo de Barras': codigo_barras, 'Ubicacion': 'P1-C10-A5'})
 

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
