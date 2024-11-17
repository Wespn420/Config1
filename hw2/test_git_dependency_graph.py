import unittest
import os
import shutil
from git_dependency_graph import GitDependencyGraph


class TestGitDependencyGraph(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом: создаём тестовый репозиторий."""
        self.test_repo_path = "test_repo"
        self.output_path = "test_output_graph"
        self.graphviz_path = "/usr/bin"

        # Создаём каталог для тестового репозитория
        os.makedirs(self.test_repo_path, exist_ok=True)
        git_dir = os.path.join(self.test_repo_path, ".git")
        os.makedirs(git_dir, exist_ok=True)

        # Создаём фиктивный HEAD и несколько объектов
        with open(os.path.join(git_dir, "HEAD"), "w") as f:
            f.write("ref: refs/heads/master\n")

        refs_heads_dir = os.path.join(git_dir, "refs", "heads")
        os.makedirs(refs_heads_dir, exist_ok=True)

        # Добавляем фиктивный коммит
        commit_sha = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
        self.create_git_object(commit_sha, b"commit 1234\0parent abcdef1234567890\n\nTest commit")

        with open(os.path.join(refs_heads_dir, "master"), "w") as f:
            f.write(commit_sha)

        # Создаём объект графа
        self.graph = GitDependencyGraph(self.test_repo_path, self.output_path, self.graphviz_path)

    def create_git_object(self, sha, content):
        """Создаёт объект Git в каталоге objects."""
        git_objects_dir = os.path.join(self.test_repo_path, ".git", "objects", sha[:2])
        os.makedirs(git_objects_dir, exist_ok=True)
        object_path = os.path.join(git_objects_dir, sha[2:])
        with open(object_path, "wb") as f:
            f.write(zlib.compress(content))

    def tearDown(self):
        """Удаляет тестовые данные после каждого теста."""
        shutil.rmtree(self.test_repo_path)
        if os.path.exists(f"{self.output_path}.png"):
            os.remove(f"{self.output_path}.png")

    def test_get_git_dir(self):
        """Тестирует нахождение .git каталога."""
        git_dir = self.graph.get_git_dir()
        self.assertTrue(os.path.isdir(git_dir))

    def test_read_object(self):
        """Тестирует чтение объекта Git."""
        sha = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
        content = self.graph.read_object(sha)
        self.assertIn(b"commit", content)
        self.assertIn(b"parent", content)

    def test_parse_commit(self):
        """Тестирует парсинг содержимого коммита."""
        commit_data = b"commit 1234\0parent abcdef1234567890\n\nTest commit"
        parents = self.graph.parse_commit(commit_data)
        self.assertEqual(parents, ["abcdef1234567890"])

    def test_collect_dependencies(self):
        """Тестирует сбор зависимостей."""
        result = self.graph.collect_dependencies()
        self.assertTrue(result)
        self.assertIn("a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0", self.graph.dependencies)

    def test_build_graph(self):
        """Тестирует построение графа."""
        self.graph.collect_dependencies()
        self.graph.build_graph()
        self.assertTrue(os.path.exists(f"{self.output_path}.png"))

    def test_generate_dependency_graph(self):
        """Тестирует полный процесс генерации графа зависимостей."""
        self.graph.generate_dependency_graph()
        self.assertTrue(os.path.exists(f"{self.output_path}.png"))

    def test_invalid_repo_path(self):
        """Тестирует ошибку при неправильном пути к репозиторию."""
        invalid_graph = GitDependencyGraph("invalid_path", self.output_path, self.graphviz_path)
        with self.assertRaises(FileNotFoundError):
            invalid_graph.get_git_dir()

    def test_user_input(self):
        """Тестирует обработку пользовательского ввода."""
        repo_path = "test_repo"
        output_path = "test_output_graph"
        graphviz_path = "/usr/bin"
        graph = GitDependencyGraph(repo_path, output_path, graphviz_path)
        self.assertEqual(graph.repo_path, repo_path)
        self.assertEqual(graph.output_path, output_path)
        self.assertEqual(graph.graphviz_path, graphviz_path)


if __name__ == "__main__":
    unittest.main()
