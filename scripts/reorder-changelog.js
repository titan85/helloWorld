const fs = require('fs');

// Lee el contenido del changelog
const changelog = fs.readFileSync('CHANGELOG.md', 'utf8');

// Divide el changelog por versión
const versions = changelog.split(/^## /gm).map((section, i) => i > 0 ? '## ' + section : section);

// Reordena los commits en cada versión
const reorderedVersions = versions.map((version) => {
    if (!version.startsWith('## ')) return version;
    
    // Divide por líneas y encuentra la lista de commits
    const lines = version.split('\n');
    const title = lines[0];
    const commits = lines.slice(1).filter(line => line.trim() !== '');

    // Reordena los commits en orden inverso
    const sortedCommits = commits.reverse();

    return [title, ...sortedCommits].join('\n');
});

// Une todas las versiones
const newChangelog = reorderedVersions.join('\n');

// Escribe el changelog actualizado
fs.writeFileSync('CHANGELOG.md', newChangelog);
