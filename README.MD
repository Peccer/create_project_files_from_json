# Automated Project Generation with JSON + `create_project.py`

This repository demonstrates how to **automate the creation of an entire project** (folders and files) by having ChatGPT output a **JSON representation** of your code (TESTED on OpenAi's o1), then using a simple Python script to convert that JSON into real directories and files on your machine.

## Why?
I like to ask ChatGPT to provide the code of complete projects. Creating folders, files and copy- pasting the code is boring so I wanted to automate part of it!

## 1. How It Works

1. **ChatGPT Prompt** – You provide ChatGPT the prompt (see file "prompt.txt" or just copy it from section 2 in this readme), instructing it to output project code in a single JSON object where each folder is a key (with nested JSON for subfolders) and each file is a key-value pair (filename → file content).

2. **Generate JSON** – ChatGPT returns a large JSON structure with all your source code embedded as strings.

3. **Create Project Script** – You copy the JSON into a local file, which has to be named `project.json` and then run the Python script `create_project.py` to “unpack” that JSON into actual folders and files. You can run the python script by opening your CLI and run `python create_project.py`. More detailed instructions below.

4. **Done!** – Your project folder is now ready, with all files containing the correct content.

---

## 2. The Prompt

Below is a **general-purpose prompt** you can use with ChatGPT (or any ChatGPT) to produce a valid JSON structure containing your entire project. **Copy-paste** this prompt whenever you want to generate a new project automatically:

---

```
I’d like you to provide the entire project code in a single valid JSON object. 

Each top-level key represents either:
- A folder (which is itself a JSON object), or
- A file (with its content as a string).

Important details:

1. Do NOT use any duplicate folder names at the same level. For example, if you have a `backend` folder, it appears only once. 
2. Each folder (e.g., `backend`, `frontend`) may contain multiple files like "Dockerfile", "main.py", etc. The file's entire code must be in the string value of that key.
3. Top-level files (like "cloudbuild.yaml", "README.md", "setup.py") should appear directly in the JSON, not inside a subfolder.
4. Return only valid JSON — no Markdown code fences or extra explanations.
5. Escape any special characters so the JSON can be parsed by `json.loads(...)` without errors.
6. No duplicate keys. If a folder is named "frontend", it should only appear once.

An example structure (shortened) might be:
{
  "backend": {
    "Dockerfile": "...",
    "main.py": "...",
    "requirements.txt": "..."
  },
  "frontend": {
    "Dockerfile": "...",
    "app.py": "...",
    "requirements.txt": "..."
  },
  "cloudbuild.yaml": "...",
  "README.md": "...",
  "setup.py": "..."
}

Please output only the JSON.
```

---

## 3. Using `create_project.py`

1. **Save ChatGPT Output as `project.json`**  
   Once you get the JSON from ChatGPT, copy all of it (just the JSON structure) into a file named `project.json`.

2. **Have `create_project.py` in the same folder**  
   Make sure your working directory contains both `project.json` **and** `create_project.py`.

3. **Run the Script**  
   From a terminal/command prompt, run:
   ```bash
   python create_project.py
   ```
   The script will:
   - Parse `project.json`
   - Create all subfolders
   - Write each file’s content in the right place

4. **Check Your New Project**  
   A new folder (named `my_project` by default in the script) will appear. Inside, you’ll see your entire code structure as specified in `project.json`.

Here is a reference `create_project.py`:

```python
import os
import json

def create_files(base_path, structure):
    """
    Recursively creates files and folders based on a JSON structure.
    :param base_path: The folder where everything should be created.
    :param structure: A dict representing the folder/file structure.
    """
    os.makedirs(base_path, exist_ok=True)
    
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # content is another directory
            create_files(path, content)
        else:
            # content is a file (string)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    with open("project.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    project_folder = "my_project"
    create_files(project_folder, data)
    print(f"Project files created in '{project_folder}'!")
```

Feel free to customize the script to change the default project folder name or handle edge cases.

---

## 4. Summary

1. Prompt ChatGPT to produce a **structured JSON** of your entire codebase.  
2. Save that JSON to `project.json`.  
3. Use `create_project.py` to automatically convert that JSON into real folders and files.  
4. **No more** manual copy-pasting or folder creation—instant code scaffolding!

Happy coding!