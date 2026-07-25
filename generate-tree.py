import os

# Liste des dossiers et fichiers à ignorer
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', '.idea', '.vscode', 'dist', 'build'}
IGNORE_FILES = {'.DS_Store', 'generate_tree.py', 'structure_projet.md'}

def generate_tree(dir_path, prefix=""):
    """
    Génère l'arborescence visuelle avec les caractères d'arborescence (├──, └──, │).
    """
    try:
        items = os.listdir(dir_path)
    except PermissionError:
        return ""

    # Filtrer les éléments ignorés
    filtered_items = [
        item for item in items 
        if item not in IGNORE_DIRS and item not in IGNORE_FILES
    ]
    
    # Séparer dossiers et fichiers pour afficher les dossiers en premier
    dirs = sorted([d for d in filtered_items if os.path.isdir(os.path.join(dir_path, d))])
    files = sorted([f for f in filtered_items if os.path.isfile(os.path.join(dir_path, f))])
    sorted_items = dirs + files

    count = len(sorted_items)
    tree_str = ""

    for index, item in enumerate(sorted_items):
        is_last = (index == count - 1)
        connector = "└── " if is_last else "├── "
        full_path = os.path.join(dir_path, item)

        if os.path.isdir(full_path):
            tree_str += f"{prefix}{connector}{item}/\n"
            # Indentation pour les sous-dossiers
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_str += generate_tree(full_path, new_prefix)
        else:
            tree_str += f"{prefix}{connector}{item}\n"

    return tree_str

if __name__ == "__main__":
    project_root = os.getcwd()
    project_name = os.path.basename(project_root)

    output = f"{project_name}/\n" + generate_tree(project_root)

    print("\n--- Organisation du projet ---\n")
    print(output)

    # Sauvegarde dans un fichier texte/markdown
    with open("structure_projet.md", "w", encoding="utf-8") as f:
        f.write("```text\n" + output + "```\n")

    print("👉 Arborescence enregistrée dans 'structure_projet.md' !")