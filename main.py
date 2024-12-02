import os
import json
from modules.classes import (
    ImageProcessor,
    ParticleCalculator,
    LatexManager,
    ExcelExporter,
)


def get_sample_paths(directory="data", prefix="sample"):
    """
    Generates a list of file paths in a specified directory that begin with a given prefix.

    Args:
        directory (str): Directory to search for files.
        prefix (str): Prefix of the file names to search for.

    Returns:
        list: List of complete paths of the files that meet the criteria.
    """
    # Verificar que el directorio existe
    if not os.path.exists(directory):
        raise FileNotFoundError(f"[!] The directory '{directory}' does not exist.")

    # Buscar archivos que comiencen con el prefijo especificado
    sample_files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.startswith(prefix) and file.endswith(".png")
    ]

    return sample_files


def update_json_section(info_path, section, key, value):
    """
    Updates a specific section of the JSON file with a new piece of data.

    Args:
        info_path (str): Path of the info folder.
        section (str): Section to update (“reference” or “samples”).
        key (str): Key to identify the data within the section.
        value (any): Value to store associated to the key.

    Raises:
        ValueError: If the section is not valid.
    """
    json_path = os.path.join(info_path, "results.json")

    # Validar sección
    if section not in ["reference", "samples"]:
        raise ValueError(
            f"Invalid section: {section}. Must be 'reference' or 'samples'."
        )

    # Leer datos existentes
    with open(json_path, "r") as json_file:
        content = json.load(json_file)

    # Actualizar la sección correspondiente
    if section == "reference":
        content["reference"][key] = value
    elif section == "samples":
        # Si no existe un diccionario para el sample, inicializarlo
        if key not in content["samples"]:
            content["samples"][key] = {}
        content["samples"][key] = value

    # Escribir de vuelta al archivo
    with open(json_path, "w") as json_file:
        json.dump(content, json_file, indent=4)
    print(f"[*] Updated: section '{section}', key '{key}'.")


manager = LatexManager()
figures_path, info_path, base_path = manager.create_directory_structure()
print(f"[*] The images will be saved in: {figures_path}")
print(f"[*] The JSON file is located in: {info_path}")

xls_exp = ExcelExporter(base_path)

# Procesar referencia
reference_path = "data/reference.png"
processor_ref = ImageProcessor(reference_path, figures_path, info_path)
# Calcular la escala mostrando solo algunos pasos
processor_ref.calculate_scale(
    real_length=200,
    show_original=False,
    show_binary=False,
    show_contours=False,
    show_bar=False,
)

# Generar dinámicamente las rutas de las imágenes de muestra
sample_paths = get_sample_paths()

# Iterar sobre las imágenes de muestra
for sample_path in sample_paths:
    sample_name = os.path.basename(sample_path).split(".")[
        0
    ]  # Extraer solo el nombre base del archivo
    print(f"\n[*] Processing: {sample_path}")

    # Instanciar el procesador para la imagen actual
    processor_sample = ImageProcessor(sample_path, figures_path, info_path)
    processor_sample.scale = processor_ref.scale  # Aplicar la escala de referencia

    # Procesar la imagen
    processor_sample.obtain_particles()
    processor_sample.visualize_contours_and_centroids()

    # Calcular las propiedades de las partículas
    calculator = ParticleCalculator(processor_sample.particles, figures_path, info_path)
    print(calculator)
    calculator.find_closest_pair_Delaunay()

    # Mostrar resultados
    print(f"[*] Minimum distance: {calculator.min_distance:.2f} um")
    calculator.plot_particles(show_plot=False, show_closest=True, show_mesh=True)

    sample_data = {
        "particles_detected": len(processor_sample.particles.particle_list),
        "combinations": calculator.combinations,
        "min_distance": calculator.min_distance,
        "distances": calculator.distances,
        "image_path": sample_path,
    }
    update_json_section(info_path, "samples", sample_name, sample_data)

scale = processor_ref.scale
samples_num = len(sample_paths)

update_json_section(info_path, "reference", "scale", {"unit": "um", "value": scale})
update_json_section(info_path, "reference", "image_path", "data/reference.png")

xls_exp.process_json_to_excel()
