import re
import subprocess

def ordenar_changelog(filepath):
    # Obtener el orden cronológico de los commits desde Git
    commit_order = subprocess.check_output(
        ["git", "log", "--pretty=format:%h"],
        universal_newlines=True
    ).splitlines()

    with open(filepath, 'r') as file:
        content = file.read()

    # Separar el contenido en secciones por versión
    versions = re.split(r"(## \[\d+\.\d+\.\d+\].*?\n)", content)

    ordered_content = versions[0]  # Guardar contenido antes de la primera versión

    for i in range(1, len(versions), 2):
        version_header = versions[i]
        commits_text = versions[i + 1]

        # Extraer y ordenar los commits de esta sección
        commit_texts = commits_text.strip().split("\n")
        sorted_commits = sorted(
            commit_texts,
            key=lambda x: commit_order.index(re.search(r'\[([a-f0-9]{7})\]', x).group(1)) 
            if re.search(r'\[([a-f0-9]{7})\]', x) and re.search(r'\[([a-f0-9]{7})\]', x).group(1) in commit_order
            else float('inf')
        )
        
        ordered_content += version_header + "\n".join(sorted_commits) + "\n"

    with open(filepath, 'w') as file:
        file.write(ordered_content)

# Ejecutar el script con la ruta absoluta al archivo CHANGELOG.md
ordenar_changelog('CHANGELOG.md')
