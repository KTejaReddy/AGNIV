import os
import shutil
from app.core.engine.capability_manager import capability_manager

async def create_file(params):
    path = params.get("path")
    content = params.get("content", "")
    with open(path, "w") as f:
        f.write(content)
    return {"status": "success", "path": path}

async def create_folder(params):
    path = params.get("path")
    os.makedirs(path, exist_ok=True)
    return {"status": "success", "path": path}

async def rename_path(params):
    src = params.get("source")
    dest = params.get("destination")
    os.rename(src, dest)
    return {"status": "success"}

async def copy_path(params):
    src = params.get("source")
    dest = params.get("destination")
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return {"status": "success"}

async def move_path(params):
    src = params.get("source")
    dest = params.get("destination")
    shutil.move(src, dest)
    return {"status": "success"}

async def delete_path(params):
    path = params.get("path")
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
    return {"status": "success"}

async def read_text_file(params):
    path = params.get("path")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return {"status": "success", "content": content}

async def search_files(params):
    directory = params.get("directory", os.path.expanduser("~"))
    query = params.get("query", "").lower()
    results = []
    # Limit search to avoid hanging
    for root, dirs, files in os.walk(directory):
        for name in files:
            if query in name.lower():
                results.append(os.path.join(root, name))
        if len(results) >= 50:
            break
    return {"status": "success", "results": results}

async def open_file(params):
    path = params.get("path")
    os.startfile(path)
    return {"status": "success"}

async def reveal_in_explorer(params):
    path = params.get("path")
    import subprocess
    subprocess.Popen(f'explorer /select,"{path}"')
    return {"status": "success"}

def register():
    capability_manager.register_capability("CREATE_FILE", "1.0", "Creates a file", create_file)
    capability_manager.register_capability("CREATE_FOLDER", "1.0", "Creates a folder", create_folder)
    capability_manager.register_capability("RENAME_PATH", "1.0", "Renames a file or folder", rename_path)
    capability_manager.register_capability("COPY_PATH", "1.0", "Copies a file or folder", copy_path)
    capability_manager.register_capability("MOVE_PATH", "1.0", "Moves a file or folder", move_path)
    capability_manager.register_capability("DELETE_PATH", "1.0", "Deletes a file or folder", delete_path)
    capability_manager.register_capability("READ_TEXT_FILE", "1.0", "Reads text from a file", read_text_file)
    capability_manager.register_capability("SEARCH_FILES", "1.0", "Searches files in a directory", search_files)
    capability_manager.register_capability("OPEN_FILE", "1.0", "Opens a file with default program", open_file)
    capability_manager.register_capability("REVEAL_IN_EXPLORER", "1.0", "Reveals file in explorer", reveal_in_explorer)
