import unittest
import os
from parser import parse_file, write_toml
import toml

# Тестирование парсера TOML
class TestConfigParser(unittest.TestCase):
    # Установка тестовой среды
    def setUp(self):
        self.test_output = "test_output.toml"
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        
    # Очистка тестовой среды
    def tearDown(self):
        if os.path.exists(self.test_output):
            os.remove(self.test_output)

    # Тестирование простого конфигурационного файла
    def test_simple_config(self):
        # Тестирование ввода-вывода для простого конфигурационного файла
        config_path = os.path.join(self.test_dir, 'examples', 'simple_config.txt')
        data = parse_file(config_path)
        write_toml(data, self.test_output)
        
        # Чтение сгенерированного TOML и проверка содержимого
        with open(self.test_output, 'r') as f:
            toml_data = toml.load(f)
            
        # Проверка базовых значений
        self.assertEqual(toml_data['constant_value'], 42)
        self.assertEqual(toml_data['array_value'], [1, 2, 3])

    # Тестирование сложных выражений
    def test_complex_expressions(self):
        # Тестирование ввода-вывода для сложных выражений
        config_path = os.path.join(self.test_dir, 'examples', 'complex_expressions.txt')
        data = parse_file(config_path)
        write_toml(data, self.test_output)
        
        # Чтение сгенерированного TOML и проверка содержимого
        with open(self.test_output, 'r') as f:
            toml_data = toml.load(f)
            
        # Проверка вычисленных выражений
        self.assertEqual(toml_data['computed_value'], 10)
        self.assertEqual(toml_data['power_result'], 1024)

    # Тестирование синтаксических ошибок
    def test_syntax_errors(self):
        # Создание временного файла для тестирования синтаксических ошибок
        test_file = os.path.join(self.test_dir, 'test_syntax.txt')
        
        # Тестирование отсутствия точки с запятой в объявлении константы
        with open(test_file, 'w') as f:
            f.write('invalid_constant <- 42')
        with self.assertRaises(SyntaxError):
            parse_file(test_file)
            
        # Тестирование неверного синтаксиса массива
        with open(test_file, 'w') as f:
            f.write('array(1 2 3)')
        with self.assertRaises(SyntaxError):
            parse_file(test_file)
            
        # Очистка
        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
