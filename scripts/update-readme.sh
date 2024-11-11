# Obtener la última major versión del changelog y añadirla al principio del readme como referencia de versión productiva en curso
latest_version=$(grep -m 1 -E "^# \[\d+\.\d+\.\d+\]" CHANGELOG.md)

if [[ -z "$latest_version" ]]; then
  echo "No hay breaking changes. No se realizará ninguna modificación en README.md."
else
  # Agregar la actualización al README.md solo si hay una versión válida
  echo -e "# Current version\n## ${latest_version}\n\n$(cat README.md)" > README.md
fi
