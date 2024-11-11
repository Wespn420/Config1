import os
import subprocess
import argparse
from graphviz import Digraph

class GitDependencyGraph:
    def __init__(self, repo_path, output_path):
        self.repo_path = repo_path
        self.output_path = output_path
        self.dependencies = {}

    def collect_dependencies(self):
        """Извлекает информацию о коммитах и их родительских коммитах."""
        try:
            # Переходим в каталог репозитория и получаем историю коммитов
            os.chdir(self.repo_path)
            # Получаем список коммитов с родительскими коммитами
            log_output = subprocess.check_output(
                ["git", "log", "--pretty=format:%H %P"],
                text=True
            )
            # Обрабатываем вывод, чтобы построить словарь зависимостей
            for line in log_output.strip().split('\n'):
                commit_hash, *parents = line.split()
                self.dependencies[commit_hash] = parents
        except subprocess.CalledProcessError as e:
            print("Ошибка при получении истории коммитов:", e)
            return False
        except FileNotFoundError:
            print("Указанный путь к репозиторию не найден.")
            return False
        return True

    def build_graph(self):
        """Строит граф зависимостей в формате DOT и сохраняет в файл PNG."""
        dot = Digraph(comment="Git Dependency Graph", format="png")

        # Добавляем узлы и связи в граф
        for commit, parents in self.dependencies.items():
            dot.node(commit, commit)
            for parent in parents:
                dot.edge(commit, parent)

        # Сохраняем граф в PNG (Graphviz автоматически найдет `dot.exe`, если он доступен)
        dot.render(self.output_path, cleanup=True)

    def generate_dependency_graph(self):
        """Главная функция для генерации графа зависимостей."""
        if self.collect_dependencies():
            self.build_graph()
            print("Граф зависимостей успешно сохранён в:", self.output_path)
        else:
            print("Не удалось создать граф зависимостей.")

def main():
    parser = argparse.ArgumentParser(description="Git Dependency Graph Visualizer")
    parser.add_argument("output_path", help="Путь к файлу с изображением графа зависимостей (без расширения)")
    parser.add_argument("--repo_path", help="Путь к анализируемому git-репозиторию", default=None)

    args = parser.parse_args()

    # Запрашиваем путь к репозиторию у пользователя, если он не был передан в аргументах
    if not args.repo_path:
        args.repo_path = input("Введите путь к анализируемому git-репозиторию: ").strip()

    graph = GitDependencyGraph(args.repo_path, args.output_path)
    graph.generate_dependency_graph()

if __name__ == "__main__":
    main()
