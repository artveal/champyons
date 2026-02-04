import os

ignore = {"__pycache__", ".venv", ".git", ".pytest_cache", "tree.py", ".vscode", "README.md", }
no_recurse = {"tests", "locales"}

def print_tree(root, prefix=""):
    items = [i for i in sorted(os.listdir(root)) if i not in ignore]

    for i, name in enumerate(items):
        path = os.path.join(root, name)
        connector = "└── " if i == len(items) - 1 else "├── "
        print(prefix + connector + name)

        if os.path.isdir(path) and name not in no_recurse:
            new_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
            print_tree(path, new_prefix)

print_tree(".")