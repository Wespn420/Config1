import os
from graphviz import Digraph
import zlib


class GitDependencyGraph:
    def __init__(self, repo_path, output_path):
        self.repo_path = repo_path
        self.output_path = output_path
        self.dependencies = {}

    def get_git_dir(self):
        """Находит директорию .git в указанном репозитории."""
        git_dir = os.path.join(self.repo_path, ".git")
        if not os.path.isdir(git_dir):
            raise FileNotFoundError(f"Каталог .git не найден в репозитории: {self.repo_path}")
        return git_dir

    def read_object(self, sha):
        """Читает объект Git из .git/objects."""
        git_dir = self.get_git_dir()
        obj_dir = os.path.join(git_dir, "objects", sha[:2])  # Первые два символа — подпапка
        obj_path = os.path.join(obj_dir, sha[2:])  # Остальная часть — имя файла
        if not os.path.isfile(obj_path):
            raise FileNotFoundError(f"Объект {sha} не найден в репозитории.")
        with open(obj_path, "rb") as f:
            compressed_data = f.read()
            data = zlib.decompress(compressed_data)
        return data

    def parse_commit(self, data):
        """Парсит содержимое объекта коммита."""
        lines = data.decode().split("\n")
        parents = []
        for line in lines:
            if line.startswith("parent "):
                parents.append(line.split()[1])  # SHA родительского коммита
            elif line == "":  # Конец заголовков
                break
        return parents

    def collect_dependencies(self):
        """Собирает зависимости коммитов, обходя историю из HEAD."""
        git_dir = self.get_git_dir()
        head_path = os.path.join(git_dir, "HEAD")
        if not os.path.isfile(head_path):
            raise FileNotFoundError("Файл HEAD не найден. Репозиторий повреждён?")

        # Получаем текущую ссылку (ref) или SHA коммита
        with open(head_path, "r") as f:
            ref = f.readline().strip()
        if ref.startswith("ref:"):
            ref_path = os.path.join(git_dir, ref[5:])
            if not os.path.isfile(ref_path):
                raise FileNotFoundError(f"Файл ref {ref_path} не найден.")
            with open(ref_path, "r") as f:
                current_commit = f.readline().strip()
        else:
            current_commit = ref  # Если в HEAD уже прямой SHA

        # Рекурсивно обходим историю коммитов
        to_visit = [current_commit]
        visited = set()

        while to_visit:
            sha = to_visit.pop()
            if sha in visited:
                continue
            visited.add(sha)

            try:
                data = self.read_object(sha)
                parents = self.parse_commit(data)
                self.dependencies[sha] = parents
                to_visit.extend(parents)  # Добавляем родителей для дальнейшего обхода
            except Exception as e:
                print(f"Ошибка при обработке коммита {sha}: {e}")

        return True

    def build_graph(self):
        """Создаёт граф зависимости в формате DOT и сохраняет в файл."""
        print("Создание графа зависимостей...")
        dot = Digraph(comment="Git Dependency Graph", format="png")

        # Добавляем узлы и связи в граф
        for commit, parents in self.dependencies.items():
            dot.node(commit, commit)
            for parent in parents:
                dot.edge(commit, parent)

        dot.render(self.output_path, cleanup=True)
        print(f"Граф зависимостей успешно сохранён в: {self.output_path}.png")

    def generate_dependency_graph(self):
        """Главная функция для генерации графа зависимостей."""
        if self.collect_dependencies():
            print(f"Зависимости успешно собраны. Создаём граф...")
            self.build_graph()
        else:
            print("Не удалось создать граф зависимостей.")


def main():
    # Запрос путей у пользователя
    repo_path = input("Введите путь к анализируемому git-репозиторию: ").strip()
    output_path = input("Введите путь для сохранения изображения графа (без расширения): ").strip()

    print(f"\nНачинаем обработку репозитория: {repo_path}")
    print(f"Файл графа зависимостей будет сохранён в: {output_path}.png")

    # Создаём объект графа и запускаем процесс
    graph = GitDependencyGraph(repo_path, output_path)
    graph.generate_dependency_graph()


if __name__ == "__main__":
    main()
