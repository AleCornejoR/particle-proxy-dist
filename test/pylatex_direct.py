from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape


def create_pdf():
    # Crear el documento
    doc = Document("generated_doc")

    # Agregar contenido
    doc.preamble.append(Command("title", "Mi Documento Generado con PyLaTeX"))
    doc.preamble.append(Command("author", "Tu Nombre"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))

    with doc.create(Section("Introducción")):
        doc.append("Este es un ejemplo de documento generado con Python y LaTeX.")
        with doc.create(Subsection("Subsección")):
            doc.append(italic("Esto es texto en cursiva."))
            doc.append(" También puedes agregar ecuaciones, gráficos y más.")

    # Generar el PDF
    doc.generate_pdf("output", clean_tex=False)


create_pdf()
