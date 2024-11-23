from pathlib import Path

def list_directory_structure(path, indent=0):
    p = Path(path)
    for item in p.iterdir():
        print(' ' * indent + item.name)
        # If the item is a directory, recursively list its contents
        if item.is_dir():
            list_directory_structure(item, indent + 4)

# Specify the path you want to inspect
directory_path = 'app'
list_directory_structure(directory_path)

