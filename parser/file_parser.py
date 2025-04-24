import ast
import os


def parse_imports(file_path, root_path=None):
    """
    Parses a Python file and extracts import statements.
    If root_path is provided, resolves relative imports.

    Returns list of (module, symbol)
    """
    imports = []
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            node = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            print(f"[WARN] Syntax error while parsing {file_path}")
            return imports

    for stmt in ast.walk(node):
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                imports.append((alias.name, None))

        elif isinstance(stmt, ast.ImportFrom):
            module = stmt.module
            if stmt.level > 0 and root_path:
                abs_dir = os.path.dirname(os.path.abspath(file_path))
                rel_parts = os.path.relpath(abs_dir, root_path).split(os.sep)
                base_parts = rel_parts[: len(rel_parts) - stmt.level + 1]
                if module:
                    full_module = ".".join(base_parts + [module])
                else:
                    full_module = ".".join(base_parts)
            else:
                full_module = module

            for alias in stmt.names:
                imports.append((full_module, alias.name))

    return imports
