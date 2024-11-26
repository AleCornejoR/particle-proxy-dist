import os
from pathlib import Path
import cv2


def preprocess_images(input_dir, output_dir, target_resolution=(344, 345)):
    """
    Preprocesa imágenes: elimina bordes transparentes, redimensiona y guarda los resultados.

    Args:
        input_dir (str): Directorio de entrada con imágenes originales.
        output_dir (str): Directorio de salida para imágenes procesadas.
        target_resolution (tuple): Resolución deseada (ancho, alto) en píxeles.
    """
    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Iterar sobre las imágenes en el directorio de entrada
    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        if not os.path.isfile(input_path):
            continue

        # Leer la imagen
        img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

        if img is None:
            print(f"No se pudo cargar la imagen: {file_name}")
            continue

        # Detectar y eliminar bordes transparentes
        if img.shape[2] == 4:  # Si tiene canal alfa
            alpha_channel = img[:, :, 3]
            _, binary_mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)
            x, y, w, h = cv2.boundingRect(binary_mask)
            img = img[y : y + h, x : x + w]

        # Redimensionar la imagen a la resolución deseada
        img_resized = cv2.resize(img, target_resolution, interpolation=cv2.INTER_AREA)

        # Guardar la imagen procesada
        cv2.imwrite(output_path, img_resized)
        print(f"Procesada y guardada: {output_path}")


if __name__ == "__main__":
    # Directorios
    script_dir = Path(__file__).parent
    input_dir = script_dir / "pre_data"
    output_dir = script_dir.parent / "data"

    # Preprocesar imágenes
    preprocess_images(input_dir, output_dir)
