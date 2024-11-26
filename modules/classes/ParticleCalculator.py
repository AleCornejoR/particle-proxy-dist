import matplotlib.pyplot as plt
import math
from itertools import combinations
from scipy.spatial import Delaunay


class ParticleCalculator:
    """
    Class to perform calculations and analysis on particles.
    """

    def __init__(self, particles):
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

    def __repr__(self):
        """
        Chain representation of the ParticleCalculator class.
        """
        return f"ParticleCalculator with {len(self.particles.particle_list)} particles."

    def plot_particles(self, show_closest=False, show_mesh=False):
        """
        Plots the particles and optionally highlights the closest pair and displays a triangular mesh connecting the particles.
        and displays a triangular mesh connecting the particles.

        Args:
            show_closest (bool): if True, shows the closest pair and the line between them.
            show_mesh (bool): If True, displays a triangle mesh between all particles.
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
        plt.show()

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

        min_distance = float("inf")
        closest_pair = None

        # Generar todas las combinaciones de pares de partículas
        for p1, p2 in combinations(self.particles.particle_list, 2):
            distance = math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_pair = (p1, p2)

        # Actualizar la pareja más cercana
        self.closest_pair = closest_pair
        self.min_distance = min_distance
