import unittest
from visual_graph import get_commits, build_dependency_graph
from graphviz import Digraph

class TestDependencyGraph(unittest.TestCase):
    def test_get_commits(self):
        """
        Тест для функции get_commits: проверяем, что функция правильно парсит данные коммитов.
        """
        # Моковые данные, представляющие вывод git log
        mock_data = "abc123 def456\ndef456\n"
        
        # Подмена вывода subprocess.run с использованием моковых данных
        with unittest.mock.patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = mock_data
            result = get_commits("dummy_repo_path")
        
        expected_result = {
            "abc123": ["def456"],
            "def456": []
        }
        self.assertEqual(result, expected_result)

    def test_build_dependency_graph(self):
        """
        Тест для функции build_dependency_graph: проверяем, что граф строится корректно.
        """
        # Моковые данные для коммитов и зависимостей
        commits = {
            "abc123": ["def456"],
            "def456": []
        }
        
        graph = build_dependency_graph(commits)
        
        # Проверяем, что созданный граф является экземпляром Digraph
        self.assertIsInstance(graph, Digraph)
        
        # Проверяем, что узлы и
