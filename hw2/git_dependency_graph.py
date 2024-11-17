import os
import subprocess
import argparse
from graphviz import Digraph

class GitDependencyGraph:
    def __init__(self, repo_path, output_path, graphviz_path):
        self.repo_path = repo_path
        self.output_path = output_path
        self.graphviz_path = graphviz_path
        self.dependencies = {}

    def collect_dependencies(self):
        """Извлекает информацию о коммитах и их родительских коммитах."""
        try:
            # Проверяем наличие репозитория
            if not os.path.isdir(self.repo_path):
                raise FileNotFoundError(f"Путь к репозиторию не найден: {self.repo_path}")
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
        except FileNotFoundError as e:
            print(e)
            return False
        return True

    def build_graph(self):
        """Строит граф зависимостей в формате DOT и сохраняет в файл PNG."""
        dot = Digraph(comment="Git Dependency Graph", format="png")

        # Добавляем папку Graphviz в PATH, если она указана
        if self.graphviz_path:
            os.environ["PATH"] += os.pathsep + self.graphviz_path

        # Добавляем узлы и связи в граф
        for commit, parents in self.dependencies.items():
            dot.node(commit, commit)
            for parent in parents:
                dot.edge(commit, parent)

        # Сохраняем граф в PNG
        dot.render(self.output_path, cleanup=True)

    def generate_dependency_graph(self):
        """Главная функция для генерации графа зависимостей."""
        print(f"Начинаем обработку репозитория: {self.repo_path}")
        print(f"Файл графа зависимостей будет сохранён в: {self.output_path}.png")
        if self.graphviz_path:
            print(f"Используется Graphviz по пути: {self.graphviz_path}")

        if self.collect_dependencies():
            self.build_graph()
            print("Граф зависимостей успешно сохранён!")
        else:
            print("Не удалось создать граф зависимостей.")

def main():
    parser = argparse.ArgumentParser(description="Git Dependency Graph Visualizer")
    parser.add_argument("--output_path", help="Путь к файлу с изображением графа зависимостей (без расширения)")
    parser.add_argument("--repo_path", help="Путь к анализируемому git-репозиторию")
    parser.add_argument("--graphviz_path", help="Путь к программе для визуализации графов Graphviz")

    args = parser.parse_args()

    # Проверка и запрос пути к Graphviz
    graphviz_path = args.graphviz_path
    if not graphviz_path:
        graphviz_path = input("Введите путь к программе Graphviz (например, C:\\Program Files\\Graphviz\\bin): ").strip()

    # Проверка и запрос пути к репозиторию
    repo_path = args.repo_path
    if not repo_path:
        repo_path = input("Введите путь к анализируемому git-репозиторию: ").strip()

    # Проверка и запрос пути к файлу с изображением
    output_path = args.output_path
    if not output_path:
        output_path = input("Введите путь для сохранения изображения графа (без расширения): ").strip()

    # Проверяем существование пути к репозиторию
    if not os.path.isdir(repo_path):
        print(f"Ошибка: Указанный путь к репозиторию не существует: {repo_path}")
        return

    # Проверяем, что путь сохранения не является директорией
    if os.path.isdir(output_path):
        print(f"Ошибка: Указанный путь {output_path} является директорией. Укажите имя файла без расширения.")
        return

    # Проверяем, что родительский каталог для файла с изображением существует
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"Ошибка: Путь к выходному файлу не существует: {output_dir}")
        return

    # Создаем объект и генерируем граф
    graph = GitDependencyGraph(repo_path, output_path, graphviz_path)
    graph.generate_dependency_graph()

if __name__ == "__main__":
    main()
