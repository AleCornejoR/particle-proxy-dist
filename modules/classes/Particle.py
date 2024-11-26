class Particle:
    """
    Representa una partícula detectada en una imagen.
    """

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):

        return f"Particle(id={self.id}, position: X:{self.x}, Y:{self.y})"
