import cv2
from pyzbar.pyzbar import decode

# Carga la imagen
image = cv2.imread('D:/Labs/Jetson/inference/training/detection/cb(1)r.jpg')

# Detecta códigos de barras en la imagen
barcodes = decode(image)

# Si se encontraron códigos de barras
if barcodes:
    # Tomamos el primer código de barras detectado
    barcode = barcodes[0]

    # Extraemos las coordenadas del código de barras
    x, y, w, h = barcode.rect

    # Recortamos la imagen para incluir solo el código de barras
    barcode_image = image[y:y + h, x:x + w]

    # Guardamos la imagen recortada
    cv2.imwrite('codigo_recortado.jpg', barcode_image)

    print("Código de barras recortado y guardado como 'codigo_recortado.jpg'")
else:
    print("No se encontraron códigos de barras en la imagen")

# Cierra las ventanas de visualización de OpenCV
cv2.destroyAllWindows()