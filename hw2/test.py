import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
# Импортируем функции из основного файла
from dependency_visualizer import get_git_commits, generate_dot_graph, save_graph_to_file

class TestDependencyVisualizer(unittest.TestCase):
    
    @patch('subprocess.run')
    def test_get_git_commits(self, mock_run):
        mock_run.return_value.stdout = "a1b2c3d4\nb1c2d3e4 a1b2c3d4\n"
        commits = get_git_commits('/fake/repo')
        self.assertEqual(commits, {'a1b2c3d4': [], 'b1c2d3e4': ['a1b2c3d4']})

    def test_generate_dot_graph(self):
        commits = {'a1b2c3d4': [], 'b1c2d3e4': ['a1b2c3d4']}
        dot_graph = generate_dot_graph(commits)
        expected_dot = 'digraph G {\n    "a1b2c3d4" -> "b1c2d3e4";\n}'
        self.assertIn(expected_dot, dot_graph)

    @patch('subprocess.run')
    def test_save_graph_to_file(self, mock_run):
        dot_graph = 'digraph G {\n    "a1b2c3d4" -> "b1c2d3e4";\n}'
        output_path = '/fake/path/output.png'
