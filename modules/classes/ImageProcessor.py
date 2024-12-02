import cv2 as cv
import os
from matplotlib import pyplot as plt
from modules.classes.Particle import Particle


class Image:
    """
    Image Class
    """

    # CONSTRUCTOR
    def __init__(self, image_path):
        self.image_path = image_path
        self.original = cv.imread(image_path)  # cargamos la imagen del constructor
        self.gray = cv.cvtColor(self.original, cv.COLOR_BGR2GRAY)
        self.hsv = cv.cvtColor(self.original, cv.COLOR_BGR2HSV)  # Convertir a HSV
        self.th = None


class ParticleList:
    """
    Class for the found particles
    """

    # CONSTRUCTOR
    def __init__(self):
        self.contours = None
        self.centroids = None
        self.particle_list = None


class ImageProcessor:
    """
    Class to process images to detect particles and calculate their properties.
    """

    # CONSTRUCTOR
    def __init__(self, image_path, figures_path, info_path):
        self.image_path = image_path
        self.figures_path = figures_path
        self.info_path = info_path
        self.image = Image(self.image_path)

        self.scale: 1.0  # Escala inicial predeterminada (en um por píxel)

        self.particles = ParticleList()

    def save_image(self, image, filename):
        """
        Saves an image in the `figures_path` folder with a unique name.

        If the file already exists, an incremental numeric suffix (_1, _2, etc.) is added to it.

        Args:
            image (ndarray): The image to be saved.
            filename (str): Base name of the file (includes extension, for example, 'image.png').
        """
        if not self.figures_path:
            raise ValueError("[!] The path of figures is not defined.")

        # Separar el nombre base y la extensión del archivo
        base_name, ext = os.path.splitext(filename)
        file_path = os.path.join(self.figures_path, filename)
        counter = 1
        file_path = os.path.join(self.figures_path, f"{base_name}_{counter}{ext}")

        # Buscar un nombre único
        while os.path.exists(file_path):
            file_path = os.path.join(self.figures_path, f"{base_name}_{counter}{ext}")
            counter += 1

        # Guardar la imagen
        cv.imwrite(file_path, image)
        print(f"[*] Image saved: {file_path}")

    def visualize_step(self, image, title="Step", show_step=True):
        """
        Displays a visualization of the step taken in the image process.

        Args:
            image (ndarray): Image to display. Assumes the image is in BGR format if using OpenCV.
            title (str): Title of the visualization window.
            show_step (bool): If True, shows the visualization.
        """
        if show_step:
            # Convert BGR to RGB if the image is in OpenCV format (common for OpenCV images)
            if image.ndim == 3 and image.shape[2] == 3:  # Check if it's a color image
                image = image[:, :, ::-1]  # Convert BGR to RGB
            plt.figure(figsize=(8, 6))
            plt.imshow(image, cmap="gray" if image.ndim == 2 else None)
            plt.title(title)
            plt.axis("off")  # Turn off axis for cleaner visualization
            plt.show()

    def calculate_scale(self, real_length, **kwargs):
        """
        Calculates the image scale based on the reference bar.

        Args:
            real_length (float): real length of the bar in physical units (um).
            kwargs: Options to display intermediate steps:
                - show_original (bool): show the original image.
                - show_binary (bool): Displays the binarized image.
                - show_contours (bool): Shows the detected contours.
                - show_bar (bool): Displays the identified reference bar.
        """

        def find_reference_bar(contours):
            """
            Identifies the outline that corresponds to the reference bar.

            Args:
                contours (list): list of detected contours.

            Returns:
                np.ndarray or None: Contour of the member if found, None if not.
            """
            for contour in contours:
                x, y, w, h = cv.boundingRect(contour)
                aspect_ratio = max(w, h) / min(w, h)

                # Suponemos que la barra tiene una relación de aspecto cercana a 10:1
                if aspect_ratio > 5:
                    return contour
            return None

        # Valores por defecto para visualización
        options = {
            "show_original": True,
            "show_binary": True,
            "show_contours": True,
            "show_bar": True,
        }
        options.update(kwargs)  # Sobrescribir valores si se pasan en kwargs

        # Paso 1: Mostrar imagen original si es necesario
        self.visualize_step(
            self.image.original,
            title="Imagen Original",
            show_step=options["show_original"],
        )
        self.save_image(self.image.original, "original_reference.png")

        # Paso 2: Binarizar la imagen
        _, binary = cv.threshold(self.image.gray, 200, 255, cv.THRESH_BINARY)
        self.visualize_step(
            binary, title="Binarized Image", show_step=options["show_binary"]
        )
        self.save_image(binary, "binarized_reference.png")

        # Paso 3: Detección de contornos
        contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour_img = self.image.original.copy()
        cv.drawContours(contour_img, contours, -1, (255, 0, 0), 2)
        self.visualize_step(
            contour_img,
            title="Contours Detected",
            show_step=options["show_contours"],
        )
        self.save_image(contour_img, "contours_reference.png")

        # Paso 4: Identificar barra de referencia
        bar_contour = find_reference_bar(contours)
        if bar_contour is None:
            raise ValueError("The reference bar could not be found.")

        x, y, w, h = cv.boundingRect(bar_contour)
        bar_img = self.image.original.copy()
        cv.rectangle(bar_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        self.visualize_step(
            bar_img,
            title="Reference Bar Identified",
            show_step=options["show_bar"],
        )
        self.save_image(bar_img, "bar_reference.png")

        # Paso 5: Calcular la escala
        self.scale = real_length / max(w, h)
        print(f"[*] Calculated scale: {self.scale:.5f} um per pixel")

    def otsuS_Binarization(self):
        img = self.image.gray

        # Mejorar contraste con CLAHE
        def enhance_contrast(img):
            clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            return clahe.apply(img)

        img = enhance_contrast(img)

        # Umbralización Otsu con y sin preprocesamiento
        _, th2 = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        blur = cv.GaussianBlur(img, (3, 3), 0)
        _, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        # Dilatación para resaltar partículas pequeñas
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        th3 = cv.dilate(th3, kernel, iterations=1)

        # Combinar con un umbral manual más bajo
        _, th_manual = cv.threshold(img, 30, 255, cv.THRESH_BINARY)
        th_combined = cv.bitwise_or(th3, th_manual)

        self.image.th = th_combined
        self.save_image(th_combined, "otsu_combined.png")

        return th_combined

    def find_contours_and_centroids(self):
        img = self.image.gray
        th3 = self.otsuS_Binarization()
        # Detección de contornos en la imagen binarizada (con Otsu tras GaussianBlur)
        contours, _ = cv.findContours(th3, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Calcular centroides
        centroids = []
        for contour in contours:
            M = cv.moments(contour)
            if M["m00"] != 0:  # Evitar división por cero
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centroids.append((cx, cy))
            else:
                pass

        self.particles.contours = contours
        self.particles.centroids = centroids

        return contours, centroids

    def visualize_contours_and_centroids(self, show_plot=False):
        centroids = self.particles.centroids
        contours = self.particles.contours
        img = self.image.gray  # Imagen en escala de grises original

        # Crear imágenes independientes para contornos y centroides
        contoured_image = cv.cvtColor(img, cv.COLOR_GRAY2BGR)  # Imagen para contornos
        centroid_image = cv.cvtColor(img, cv.COLOR_GRAY2BGR)  # Imagen para centroides

        # Dibujar contornos
        for contour in contours:
            cv.drawContours(contoured_image, [contour], -1, (255, 0, 0), 1)

        # Dibujar centroides
        for centroid in centroids:
            if centroid is not None:
                cx, cy = centroid
                cv.circle(centroid_image, (cx, cy), 1, (0, 255, 0), -1)

        self.save_image(contoured_image, "contoured_image.png")
        self.save_image(centroid_image, "centroid_image.png")

        if show_plot:
            # Mostrar las imágenes
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(contoured_image)
            plt.title("Contours")
            plt.axis("off")

            plt.subplot(1, 2, 2)
            plt.imshow(centroid_image)
            plt.title("Centroids")
            plt.axis("off")

            plt.show()

    def convert_centroids_to_particles(self):
        """
        Converts the centroids into instances of the Particle class and stores them in self.particles.particle_list.
        """
        if not hasattr(self, "particles"):
            raise AttributeError(
                "The object must have a 'particles' attribute to store the list of particles."
            )

        if not hasattr(self.particles, "centroids"):
            raise AttributeError(
                "The 'particles' attribute must have a list of centroids in 'centroids'."
            )

        if not hasattr(self, "scale"):
            raise AttributeError(
                "The object must have a 'scale' attribute indicating the scale in um/pixel."
            )

        self.particles.particle_list = []  # Inicializar lista para las partículas
        for idx, (cx, cy) in enumerate(self.particles.centroids):
            # Convertir coordenadas a micrómetros
            x_um = cx * self.scale
            y_um = cy * self.scale

            # Crear instancia de Particle
            particle = Particle(id=idx, x=x_um, y=y_um)

            # Agregar la partícula a la lista
            self.particles.particle_list.append(particle)

    def obtain_particles(self):
        self.find_contours_and_centroids()
        self.convert_centroids_to_particles()
