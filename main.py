from modules.classes import ImageProcessor, ParticleCalculator


# Procesar referencia
reference_path = "data/reference.png"
processor_ref = ImageProcessor(reference_path)
# Calcular la escala mostrando solo algunos pasos
processor_ref.calculate_scale(
    real_length=200,
    show_original=False,
    show_binary=False,
    show_contours=False,
    show_bar=False,
)

# Lista de rutas de las imágenes de muestra
sample_paths = [
    "data/sample1.png",
    "data/sample2.png",
    "data/sample3.png",
    "data/sample4.png",
]

# Iterar sobre las imágenes de muestra
for sample_path in sample_paths:
    print(f"\nProcesando: {sample_path}")

    # Instanciar el procesador para la imagen actual
    processor_sample = ImageProcessor(sample_path)
    processor_sample.scale = processor_ref.scale  # Aplicar la escala de referencia

    # Procesar la imagen
    processor_sample.obtain_particles()
    processor_sample.visualize_contours_and_centroids()

    # Calcular las propiedades de las partículas
    calculator = ParticleCalculator(processor_sample.particles)
    print(calculator)
    calculator.find_closest_pair()

    # Mostrar resultados
    print(f"Distancia mínima: {calculator.min_distance:.2f} um")
    calculator.plot_particles(show_closest=True, show_mesh=True)
