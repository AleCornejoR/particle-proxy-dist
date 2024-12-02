import subprocess


def create_tex_file():
    content = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}

    \title{Mi Documento Generado con Python}
    \author{Tu Nombre}
    \date{\today}

    \begin{document}

    \maketitle

    \section{Introducci\'on}
    Este documento fue generado autom\'aticamente con Python y compilado usando LaTeX.

    \subsection{Subsecci\'on}
    Aqu\'i puedes incluir ecuaciones como $E=mc^2$ o texto personalizado.

    \end{document}
    """
    # Guardar en un archivo .tex con codificación UTF-8
    with open("output.tex", "w", encoding="utf-8") as file:
        file.write(content)

    # Compilar el archivo .tex a PDF (requiere tener pdflatex instalado)
    subprocess.run(["pdflatex", "output.tex"])


create_tex_file()
