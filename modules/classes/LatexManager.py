import os
import json
from datetime import datetime
import subprocess


class LatexManager:
    def __init__(self, output_dir="output"):
        """
        Initializes the LaTeX manager.

        Args:
            output_dir (str): base directory where the results will be saved.
        """
        self.output_dir = output_dir
        self.current_dir = None  # Ruta del directorio creado para esta ejecución
        self.figures_dir = None  # Ruta de la carpeta 'figures'

    def create_directory_structure(self):
        """
        Crea la estructura de directorios para guardar figuras y datos JSON.

        Returns:
            tuple: Path de las carpetas figures e info creadas.
        """
        # Obtener fecha actual en formato deseado
        date_str = datetime.now().strftime("%m%d%y")
        base_path = os.path.join(self.output_dir, date_str)

        # Incrementar el sufijo si ya existe la carpeta
        suffix = 1
        while os.path.exists(f"{base_path}_{suffix}"):
            suffix += 1
        base_path = f"{base_path}_{suffix}"

        # Crear carpeta principal
        os.makedirs(base_path, exist_ok=True)

        # Crear subcarpetas figures y info
        figures_path = os.path.join(base_path, "figures")
        info_path = os.path.join(base_path, "info")
        os.makedirs(figures_path, exist_ok=True)
        os.makedirs(info_path, exist_ok=True)

        # Crear archivo JSON inicial en info
        self._create_initial_json(info_path)

        return figures_path, info_path, base_path

    def _create_initial_json(self, info_path):
        """
        Crea un archivo JSON inicial para almacenar datos.

        Args:
            info_path (str): Path de la carpeta info.
        """
        initial_data = {
            "reference": {},
            "samples": {},
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "description": "Particulate analysis results",
            },
        }
        json_path = os.path.join(info_path, "results.json")
        with open(json_path, "w") as json_file:
            json.dump(initial_data, json_file, indent=4)
        print(f"[*] Initial JSON file created: {json_path}")

    def generate_pdf(self, content):
        """
        Genera un PDF a partir del contenido LaTeX proporcionado.

        Args:
            content (str): Código LaTeX para el documento.
        """
        if not self.current_dir:
            raise ValueError("Debe crear la estructura de directorios primero.")

        # Guardar el archivo .tex
        tex_path = os.path.join(self.current_dir, "results.tex")
        with open(tex_path, "w", encoding="utf-8") as tex_file:
            tex_file.write(content)

        # Compilar el archivo .tex a PDF
        try:
            subprocess.run(
                ["pdflatex", "-output-directory", self.current_dir, tex_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Error al compilar el archivo LaTeX.") from e

    def get_figures_dir(self):
        """
        Returns the path to the 'figures' folder.

        Returns:
            str: Path to the 'figures' folder.
        """
        if not self.figures_dir:
            raise ValueError("[!] You must create the directory structure first.")
        return self.figures_dir
