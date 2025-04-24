import sys
import os
from parser.repo_scanner import scan_directory
from graph.dependency_graph import DependencyGraph

DEFAULT_PATH = "tests/test_dir"


def main():
    # Get directory from CLI args or use default
    repo_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    if not os.path.exists(repo_path):
        print(f"[ERROR] Path does not exist: {repo_path}")
        return

    python_files = scan_directory(repo_path)

    graph = DependencyGraph()
    for file_path in python_files:
        graph.add_file(file_path)

    graph.build()
    graph.display()


if __name__ == "__main__":
    main()
