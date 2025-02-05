import os
import json

def create_files(base_path, structure):
    """
    Recursively creates files and folders based on a JSON structure.
    :param base_path: The folder where everything should be created.
    :param structure: A dict representing the folder/file structure.
    """
    # Ensure the base directory exists
    os.makedirs(base_path, exist_ok=True)
    
    # Iterate over items in the JSON structure
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        # If the content is another dict, it's a folder (recursively create it)
        if isinstance(content, dict):
            create_files(path, content)
        else:
            # Otherwise, it's a file. Write the content to the file.
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    # 1. Open project.json
    with open("project.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 2. Choose a name or path for the top-level project folder
    #    (Change "my_project" to whatever you want to name the folder)
    project_folder = "my_project"

    # 3. Generate all folders and files
    create_files(project_folder, data)

    # 4. Print a confirmation
    print(f"Project files created in '{project_folder}' folder.")
