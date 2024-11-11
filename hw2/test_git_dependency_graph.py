import unittest
import os
from git_dependency_graph import GitDependencyGraph

class TestGitDependencyGraph(unittest.TestCase):
    def setUp(self):
        # Используйте путь к тестовому репозиторию и тестовые файлы
        self.graph = GitDependencyGraph("test_repo", "test_output", "/usr/bin/dot")

    def test_collect_dependencies(self):
        # Проверяем успешность сбора зависимостей
        self.assertTrue(self.graph.collect_dependencies())
        # Проверяем, что хотя бы один коммит присутствует
        self.assertGreater(len(self.graph.dependencies), 0)

    def test_build_graph(self):
        # Создание графа после сбора зависимостей
        self.graph.collect_dependencies()
        self.graph.build_graph()
        # Проверка наличия выходного файла
        self.assertTrue(os.path.exists("test_output.png"))
        # Удаление тестового файла после проверки
        os.remove("test_output.png")

if __name__ == "__main__":
    unittest.main()
