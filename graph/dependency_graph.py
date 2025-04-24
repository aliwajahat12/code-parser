import os
from parser.file_parser import parse_imports


class DependencyGraph:
    def __init__(self):
        self.files = set()  # Set of absolute file paths
        self.dependencies = {}  # { file_path: set(imported_file_paths) }

    def add_file(self, file_path):
        self.files.add(os.path.abspath(file_path))

    def _module_name_from_path(self, file_path, root_path):
        rel_path = os.path.relpath(file_path, root_path)
        no_ext = os.path.splitext(rel_path)[0]
        return no_ext.replace(os.sep, '.')

    def build(self):
        root_path = os.path.commonpath(list(self.files))
        file_map = {
            self._module_name_from_path(f, root_path): f
            for f in self.files
        }

        for file_path in self.files:
            imports = parse_imports(file_path, root_path)
            self.dependencies[file_path] = set()

            for module, symbol in imports:
                if module is None:
                    continue

                for mod_name, mod_path in file_map.items():
                    if mod_name == module or (symbol and mod_name == f"{module}.{symbol}"):
                        self.dependencies[file_path].add(os.path.abspath(mod_path))

    def display(self):
        print("Dependency Graph:")
        for file_path, deps in self.dependencies.items():
            print(f"\n{os.path.relpath(file_path)} imports:")
            if not deps:
                print("  - No internal dependencies")
            for dep in deps:
                print(f"  - {os.path.relpath(dep)}")
