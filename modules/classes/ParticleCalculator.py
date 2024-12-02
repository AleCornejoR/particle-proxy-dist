import matplotlib.pyplot as plt
import math
import os
from itertools import combinations
from scipy.spatial import Delaunay


class ParticleCalculator:
    """
    Class to perform calculations and analysis on particles.
    """

    def __init__(self, particles, figures_path, info_path):
        """
        Initializes the class with the particles to be analyzed.

        Args:
            particles: object containing the list of particles and their associated attributes.
        """
        if not hasattr(particles, "particle_list"):
            raise AttributeError(
                "The 'particles' object must have a 'particle_list' attribute."
            )

        self.particles = particles
        self.closest_pair = []
        self.min_distance = 0.1
        self.figures_path = figures_path
        self.info_path = info_path
        self.distances = []
        self.combinations = 0

    def __repr__(self):
        """
        Chain representation of the ParticleCalculator class.
        """
        return f"ParticleCalculator with {len(self.particles.particle_list)} particles."

    def save_plot(self, figures_path, filename):
        """
        Saves the current matplotlib figure as an image in a specific folder.

        Always append a numeric suffix (_1, _2, etc.) to the file name.

        Args:
            figures_path (str): Directory where the image will be saved.
            filename (str): Base name of the file (includes extension, e.g. 'plot.png').
        """
        if not figures_path:
            raise ValueError("[!] The path of figures is not defined.")

        # Separar el nombre base y la extensión del archivo
        base_name, ext = os.path.splitext(filename)
        counter = 1
        file_path = os.path.join(figures_path, f"{base_name}_{counter}{ext}")

        # Buscar un nombre único
        while os.path.exists(file_path):
            counter += 1
            file_path = os.path.join(figures_path, f"{base_name}_{counter}{ext}")

        # Guardar la figura actual
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        print(f"[*] Graph saved: {file_path}")

    def plot_particles(self, show_plot=True, show_closest=False, show_mesh=False):
        """
        Plots the particles and optionally highlights the closest pair and displays a triangular mesh connecting the particles.
        and displays a triangular mesh connecting the particles.

        Args:
            show_closest (bool): if True, shows the closest pair and the line between them.
            show_mesh (bool): If True, displays a triangle mesh between all particles.
            save_filename (str): If provided, saves the plot as an image with this filename.
        """
        x_coords = [p.x for p in self.particles.particle_list]
        y_coords = [p.y for p in self.particles.particle_list]

        plt.figure(figsize=(10, 8))

        # Graficar todas las partículas
        plt.scatter(x_coords, y_coords, c="blue", s=10, label="Particles")

        # Generar malla triangular si se solicita
        if show_mesh:
            points = list(zip(x_coords, y_coords))
            triangulation = Delaunay(points)

            # Dibujar los triángulos
            for simplex in triangulation.simplices:
                plt.plot(
                    [points[simplex[0]][0], points[simplex[1]][0]],
                    [points[simplex[0]][1], points[simplex[1]][1]],
                    c="green",
                    linewidth=0.2,
                )
                plt.plot(
                    [points[simplex[1]][0], points[simplex[2]][0]],
                    [points[simplex[1]][1], points[simplex[2]][1]],
                    c="green",
                    linewidth=0.2,
                )
                plt.plot(
                    [points[simplex[2]][0], points[simplex[0]][0]],
                    [points[simplex[2]][1], points[simplex[0]][1]],
                    c="green",
                    linewidth=0.2,
                )

        # Si se debe mostrar el par más cercano y existe uno
        if show_closest and self.closest_pair:
            p1, p2 = self.closest_pair
            plt.plot(
                [p1.x, p2.x],
                [p1.y, p2.y],
                c="red",
                linestyle="--",
                label="Closest pair",
            )
            plt.scatter([p1.x, p2.x], [p1.y, p2.y], c="red", s=15, label="Closest pair")

        # Configuración de ejes
        plt.gca().invert_yaxis()  # Invertir eje Y para que crezca hacia arriba
        plt.title("Particles detected")
        plt.xlabel("Coordinate X (um)")
        plt.ylabel("Coordinate Y (um)")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")

        # Guardar el gráfico
        self.save_plot(self.figures_path, "particles_plot.png")

        # Mostrar el gráfico si show_plot es True
        if show_plot:
            plt.show()

        plt.close()

    def find_closest_pair(self):
        """
        Finds the pair of particles that are at the smallest distance from each other
        and stores it in self.closest_pair.

        Returns:
            float: the minimum distance found.
        """
        if len(self.particles.particle_list) < 2:
            print("At least two particles are needed to calculate the distance.")
            self.closest_pair = []  # Resetear por si no hay suficientes partículas
            return None

        # Reiniciar lista de distancias
        self.distances = []
        self.combinations = 0
        min_distance = float("inf")
        closest_pair = None

        # Generar todas las combinaciones de pares de partículas
        for p1, p2 in combinations(self.particles.particle_list, 2):
            self.combinations += 1  # Contar combinaciones
            distance = math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

            # Guardar la distancia en la lista
            self.distances.append(
                {
                    "pair": {p1.id: (p1.x, p1.y), p2.id: (p2.x, p2.y)},
                    "distance": distance,
                }
            )
            if distance < min_distance:
                min_distance = distance
                closest_pair = (p1, p2)

        # Actualizar la pareja más cercana
        self.closest_pair = closest_pair
        self.min_distance = min_distance

    def find_closest_pair_Delaunay(self):
        """
        Finds the pair of particles that are at the smallest distance from each other
        and stores it in self.closest_pair. Calculates distances only between particles
        that are connected in a Delaunay triangulation, ensuring no duplicate distances.
        """

        if len(self.particles.particle_list) < 2:
            print("At least two particles are needed to calculate the distance.")
            self.closest_pair = []  # Resetear por si no hay suficientes partículas
            return None

        # Reiniciar lista de distancias
        self.distances = []
        self.combinations = 0
        min_distance = float("inf")
        closest_pair = None

        # Extraer las coordenadas de las partículas
        points = [(p.x, p.y) for p in self.particles.particle_list]

        # Generar la triangulación de Delaunay
        delaunay = Delaunay(points)

        # Conjunto para almacenar bordes ya procesados
        processed_edges = set()

        # Iterar sobre los bordes de los triángulos de la malla de Delaunay
        for simplex in delaunay.simplices:
            for i, j in [(0, 1), (1, 2), (2, 0)]:  # Los 3 bordes de cada triángulo
                p1, p2 = (
                    self.particles.particle_list[simplex[i]],
                    self.particles.particle_list[simplex[j]],
                )

                # Crear una representación única del borde (ordenado para evitar duplicados)
                edge = tuple(sorted([p1.id, p2.id]))

                # Si el borde ya ha sido procesado, lo ignoramos
                if edge in processed_edges:
                    continue

                # Marcar el borde como procesado
                processed_edges.add(edge)

                distance = math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
                self.combinations += 1  # Contar combinaciones de bordes

                # Guardar la distancia en la lista
                self.distances.append(
                    {
                        "pair": {p1.id: (p1.x, p1.y), p2.id: (p2.x, p2.y)},
                        "distance": distance,
                    }
                )

                # Verificar si esta es la distancia mínima
                if distance < min_distance:
                    min_distance = distance
                    closest_pair = (p1, p2)

        # Actualizar la pareja más cercana
        self.closest_pair = closest_pair
        self.min_distance = min_distance
