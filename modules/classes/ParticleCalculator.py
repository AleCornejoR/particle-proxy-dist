import matplotlib.pyplot as plt
import math
from itertools import combinations
from scipy.spatial import Delaunay


class ParticleCalculator:
    """
    Clase para realizar cálculos y análisis sobre partículas.
    """

    def __init__(self, particles):
        """
        Inicializa la clase con las partículas a analizar.

        Args:
            particles: Objeto que contiene la lista de partículas y sus atributos asociados.
        """
        if not hasattr(particles, "particle_list"):
            raise AttributeError(
                "El objeto 'particles' debe tener un atributo 'particle_list'."
            )

        self.particles = particles
        self.closest_pair = []
        self.min_distance = 0.1

    def __repr__(self):
        """
        Representación en cadena de la clase ParticleCalculator.
        """
        return f"ParticleCalculator con {len(self.particles.particle_list)} partículas."

    def plot_particles(self, show_closest=False, show_mesh=False):
        """
        Grafica las partículas y, opcionalmente, resalta el par más cercano
        y muestra una malla triangular que conecta las partículas.

        Args:
            show_closest (bool): Si True, muestra el par más cercano y la línea entre ellos.
            show_mesh (bool): Si True, muestra una malla de triángulos entre todas las partículas.
        """
        x_coords = [p.x for p in self.particles.particle_list]
        y_coords = [p.y for p in self.particles.particle_list]

        plt.figure(figsize=(10, 8))

        # Graficar todas las partículas
        plt.scatter(x_coords, y_coords, c="blue", s=20, label="Partículas")

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
                    linewidth=0.5,
                )
                plt.plot(
                    [points[simplex[1]][0], points[simplex[2]][0]],
                    [points[simplex[1]][1], points[simplex[2]][1]],
                    c="green",
                    linewidth=0.5,
                )
                plt.plot(
                    [points[simplex[2]][0], points[simplex[0]][0]],
                    [points[simplex[2]][1], points[simplex[0]][1]],
                    c="green",
                    linewidth=0.5,
                )

        # Si se debe mostrar el par más cercano y existe uno
        if show_closest and self.closest_pair:
            p1, p2 = self.closest_pair
            plt.plot(
                [p1.x, p2.x],
                [p1.y, p2.y],
                c="red",
                linestyle="--",
                label="Par más cercano",
            )
            plt.scatter(
                [p1.x, p2.x], [p1.y, p2.y], c="red", s=20, label="Pareja más cercana"
            )

        # Configuración de ejes
        plt.gca().invert_yaxis()  # Invertir eje Y para que crezca hacia arriba
        plt.title("Partículas detectadas")
        plt.xlabel("Coordenada X (um)")
        plt.ylabel("Coordenada Y (um)")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        plt.show()

    def find_closest_pair(self):
        """
        Encuentra el par de partículas que están a la menor distancia entre sí
        y lo almacena en self.closest_pair.

        Returns:
            float: La distancia mínima encontrada.
        """
        if len(self.particles.particle_list) < 2:
            print("Se necesitan al menos dos partículas para calcular la distancia.")
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
