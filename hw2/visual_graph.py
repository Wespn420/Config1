import subprocess
import argparse
from graphviz import Digraph

def parse_arguments():
    """
    Парсинг аргументов командной строки.
    """
    parser = argparse.ArgumentParser(description="Git Dependency Graph Visualizer")
    parser.add_argument("--graphviz-path", required=True, help="Path to the Graphviz program")
    parser.add_argument("--repo-path", required=True, help="Path to the Git repository")
    parser.add_argument("--output-path", required=True, help="Path to the output image file")
    return parser.parse_args()

def get_commits(repo_path):
    """
    Получает коммиты и их родительские коммиты для создания зависимостей.
    Возвращает словарь, где ключи — хеши коммитов, а значения — списки родительских коммитов.
    """
    result = subprocess.run(
        ["git", "-C", repo_path, "log", "--pretty=format:%H %P"],
        stdout=subprocess.PIPE,
        text=True,
    )
    commits = {}
    for line in result.stdout.splitlines():
        parts = line.split()
        commits[parts[0]] = parts[1:]  # первый элемент — текущий коммит, остальные — родители
    return commits

def build_dependency_graph(commits):
    """
    Создаёт граф зависимостей с использованием библиотеки Graphviz.
    На вход принимает словарь коммитов и их родительских зависимостей.
    Возвращает объект Digraph.
    """
    dot = Digraph(comment="Commit Dependency Graph")
    for commit, parents in commits.items():
        dot.node(commit)  # добавляем узел для каждого коммита
        for parent in parents:
            dot.edge(commit, parent)  # добавляем ребро между коммитом и его родителем
    return dot

def save_graph(graph, output_path):
    """
    Сохраняет граф в формате PNG.
    """
    graph.render(output_path, format="png")
    print(f"Граф зависимостей успешно создан и сохранён в {output_path}.png")

def main():
    args = parse_arguments()
    commits = get_commits(args.repo_path)
    graph = build_dependency_graph(commits)
    save_graph(graph, args.output_path)

if __name__ == "__main__":
    main()
