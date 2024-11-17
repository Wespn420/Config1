import unittest
import os
from unittest.mock import patch, MagicMock
from git_dependency_graph import GitDependencyGraph

class TestGitDependencyGraph(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.test_repo_path = "test_repo"
        self.test_output_path = "test_output_graph"
        self.test_graphviz_path = "/usr/bin"

        # Создаем тестовый объект GitDependencyGraph
        self.graph = GitDependencyGraph(
            repo_path=self.test_repo_path,
            output_path=self.test_output_path,
            graphviz_path=self.test_graphviz_path
        )

    def test_collect_dependencies_success(self):
        """Тест успешного сбора зависимостей из git-репозитория."""
        # Mock для subprocess.check_output
        mock_output = "abc123 def456\ndef456 ghi789"
        with patch("subprocess.check_output", return_value=mock_output):
            success = self.graph.collect_dependencies()
        
        self.assertTrue(success)
        self.assertIn("abc123", self.graph.dependencies)
        self.assertEqual(self.graph.dependencies["abc123"], ["def456"])
        self.assertIn("def456", self.graph.dependencies)
        self.assertEqual(self.graph.dependencies["def456"], ["ghi789"])

    def test_collect_dependencies_git_error(self):
        """Тест ошибки при вызове git log."""
        with patch("subprocess.check_output", side_effect=Exception("Git Error")):
            success = self.graph.collect_dependencies()
        self.assertFalse(success)
        self.assertEqual(self.graph.dependencies, {})

    def test_collect_dependencies_invalid_repo_path(self):
        """Тест обработки ошибки, если путь к репозиторию неверен."""
        with patch("os.chdir", side_effect=FileNotFoundError("Path not found")):
            success = self.graph.collect_dependencies()
        self.assertFalse(success)

    def test_build_graph_success(self):
        """Тест успешного построения графа зависимостей."""
        # Устанавливаем фиктивные зависимости
        self.graph.dependencies = {
            "abc123": ["def456"],
            "def456": ["ghi789"],
        }

        # Mock для render
        with patch("graphviz.Digraph.render") as mock_render:
            self.graph.build_graph()
        
        mock_render.assert_called_once_with(self.test_output_path, cleanup=True)

    def test_build_graph_no_dependencies(self):
        """Тест построения графа при отсутствии зависимостей."""
        self.graph.dependencies = {}
        with patch("graphviz.Digraph.render") as mock_render:
            self.graph.build_graph()
        mock_render.assert_called_once_with(self.test_output_path, cleanup=True)

    def test_generate_dependency_graph_success(self):
        """Тест успешного выполнения полного цикла генерации графа."""
        # Mock для функций collect_dependencies и build_graph
        with patch.object(self.graph, "collect_dependencies", return_value=True) as mock_collect:
            with patch.object(self.graph, "build_graph") as mock_build:
                self.graph.generate_dependency_graph()

        mock_collect.assert_called_once()
        mock_build.assert_called_once()

    def test_generate_dependency_graph_collect_fail(self):
        """Тест обработки ошибки при сборе зависимостей."""
        with patch.object(self.graph, "collect_dependencies", return_value=False) as mock_collect:
            with patch.object(self.graph, "build_graph") as mock_build:
                self.graph.generate_dependency_graph()

        mock_collect.assert_called_once()
        mock_build.assert_not_called()

    def test_path_integration(self):
        """Тест корректного использования путей."""
        self.assertEqual(self.graph.repo_path, self.test_repo_path)
        self.assertEqual(self.graph.output_path, self.test_output_path)
        self.assertEqual(self.graph.graphviz_path, self.test_graphviz_path)

if __name__ == "__main__":
    unittest.main()
