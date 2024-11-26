import cv2 as cv
import numpy as np
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
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image(self.image_path)

        self.scale: 1.0  # Escala inicial predeterminada (en um por píxel)

        self.particles = ParticleList()

    def visualize_step(self, image, title="Step", show_step=True):
        """
        Displays a visualization of the step taken in the image process.

        Args:
            image (ndarray): image to display.
            title (str): Title of the visualization window.
            show_step (bool): If True, shows the visualization.
        """
        if show_step:
            cv.imshow(title, image)
            cv.waitKey(0)
            cv.destroyAllWindows()

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

        # Paso 2: Binarizar la imagen
        _, binary = cv.threshold(self.image.gray, 200, 255, cv.THRESH_BINARY)
        self.visualize_step(
            binary, title="Binarized Image", show_step=options["show_binary"]
        )

        # Paso 3: Detección de contornos
        contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour_img = self.image.gray
        cv.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
        self.visualize_step(
            contour_img,
            title="Contours Detected",
            show_step=options["show_contours"],
        )

        # Paso 4: Identificar barra de referencia
        bar_contour = find_reference_bar(contours)
        if bar_contour is None:
            raise ValueError("The reference bar could not be found.")

        x, y, w, h = cv.boundingRect(bar_contour)
        bar_img = contour_img.copy()
        cv.rectangle(bar_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        self.visualize_step(
            bar_img,
            title="Reference Bar Identified",
            show_step=options["show_bar"],
        )

        # Paso 5: Calcular la escala
        self.scale = real_length / max(w, h)
        print(f"Calculated scale: {self.scale:.5f} um per pixel")

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

    def visualize_contours_and_centroids(self):
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
