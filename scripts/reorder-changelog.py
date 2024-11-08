import re
import subprocess

def listar_versiones_y_secciones(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    # Obtener el orden cronológico de los commits desde Git
    commit_order = subprocess.check_output(
        ["git", "log", "--pretty=format:%h"],
        universal_newlines=True
    ).splitlines()

    # Detectar las versiones junto con sus contenidos
    versions = re.split(r"(# \d+\.\d+\.\d+.*?\n)", content)

    if len(versions) > 1:
        print("Versiones y secciones encontradas y ordenadas:")

        ordered_content = versions[0]  # Contenido antes de la primera versión

        # Iterar en pares (encabezado y contenido)
        for i in range(1, len(versions), 2):
            version_header = versions[i].strip()
            version_content = versions[i + 1] if i + 1 < len(versions) else ""
            ordered_content += version_header + "\n"

            print(f"\nVersión encontrada: {version_header}")

            # Detectar secciones y ordenar commits en cada sección
            sections = {
                "BREAKING CHANGES": "NO encontrada",
                "Features": "NO encontrada",
                "Bug Fixes": "NO encontrada",
                "Performance Improvements": "NO encontrada",
                "Refactoring": "NO encontrada",
                "Documentation": "NO encontrada",
                "Styles": "NO encontrada",
                "Tests": "NO encontrada",
                "Build System": "NO encontrada",
                "Continuous Integration": "NO encontrada",
                "Other": "NO encontrada"
            }

            for section in sections.keys():
                section_pattern = rf"(### {section}\n(.*?)(?=\n###|\Z))"
                section_match = re.search(section_pattern, version_content, re.S)

                if section_match:
                    sections[section] = "encontrada"
                    section_content = section_match.group(2).strip().split("\n")

                    # Extraer y ordenar commits dentro de la sección
                    sorted_commits = sorted(
                        section_content,
                        key=lambda x: commit_order.index(re.search(r'\[([a-f0-9]{7})\]', x).group(1))
                        if re.search(r'\[([a-f0-9]{7})\]', x) and re.search(r'\[([a-f0-9]{7})\]', x).group(1) in commit_order
                        else float('inf')
                    )

                    # Formatear y agregar sección con saltos de línea
                    ordered_content += f"\n\n### {section}\n\n" + "\n".join(sorted_commits) + "\n"

            ordered_content += "\n"

        # Escribir el contenido ordenado en el archivo
        with open(filepath, 'w') as file:
            file.write(ordered_content)

    else:
        print("No se encontraron versiones.")

# Ejecutar el script en el archivo CHANGELOG.md
listar_versiones_y_secciones('CHANGELOG.md')
