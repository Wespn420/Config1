import unittest
import subprocess
import os

class TestAssemblerInterpreter(unittest.TestCase):
    def setUp(self):
        # Путь к файлам
        self.assembler_path = 'assembler.py'
        self.interpreter_path = 'interpreter.py'
        self.test_program_path = 'test_program.asm'
        self.binary_output_path = 'output.bin'
        self.log_output_path = 'log.xml'
        self.result_output_path = 'result.xml'

    def test_load_const(self):
        # Создание тестовой программы для LOAD_CONST
        with open(self.test_program_path, 'w') as f:
            f.write('LOAD_CONST 123\nWRITE_MEM 0\n')

        # Запуск ассемблера
        subprocess.run(['python', self.assembler_path, self.test_program_path, self.binary_output_path, self.log_output_path], check=True)

        # Запуск интерпретатора
        subprocess.run(['python', self.interpreter_path, self.binary_output_path, self.result_output_path, '0-1'], check=True)

        # Проверка результата
        with open(self.result_output_path, 'r') as f:
            result = f.read()
        self.assertIn('<memory address="0" value="123" />', result)

    def test_read_mem(self):
        # Создание тестовой программы для READ_MEM
        with open(self.test_program_path, 'w') as f:
            f.write('LOAD_CONST 456\nWRITE_MEM 1\nREAD_MEM 1\nWRITE_MEM 2\n')

        # Запуск ассемблера
        subprocess.run(['python', self.assembler_path, self.test_program_path, self.binary_output_path, self.log_output_path], check=True)

        # Запуск интерпретатора
        subprocess.run(['python', self.interpreter_path, self.binary_output_path, self.result_output_path, '1-3'], check=True)

        # Проверка результата
        with open(self.result_output_path, 'r') as f:
            result = f.read()
        self.assertIn('<memory address="2" value="456" />', result)

    def test_write_mem(self):
        # Создание тестовой программы для WRITE_MEM
        with open(self.test_program_path, 'w') as f:
            f.write('LOAD_CONST 789\nWRITE_MEM 3\n')

        # Запуск ассемблера
        subprocess.run(['python', self.assembler_path, self.test_program_path, self.binary_output_path, self.log_output_path], check=True)

        # Запуск интерпретатора
        subprocess.run(['python', self.interpreter_path, self.binary_output_path, self.result_output_path, '3-4'], check=True)

        # Проверка результата
        with open(self.result_output_path, 'r') as f:
            result = f.read()
        self.assertIn('<memory address="3" value="789" />', result)

    def test_shift_left(self):
        # Создание тестовой программы для SHIFT_LEFT
        with open(self.test_program_path, 'w') as f:
            f.write('LOAD_CONST 1\nWRITE_MEM 4\nLOAD_CONST 2\nWRITE_MEM 5\nREAD_MEM 4\nREAD_MEM 5\nSHIFT_LEFT 4\nWRITE_MEM 4\n')

        # Запуск ассемблера
        subprocess.run(['python', self.assembler_path, self.test_program_path, self.binary_output_path, self.log_output_path], check=True)

        # Запуск интерпретатора
        subprocess.run(['python', self.interpreter_path, self.binary_output_path, self.result_output_path, '4-6'], check=True)

        # Проверка результата
        with open(self.result_output_path, 'r') as f:
            result = f.read()
        self.assertIn('<memory address="4" value="4" />', result)

    def tearDown(self):
        # Удаление временных файлов
        os.remove(self.test_program_path)
        os.remove(self.binary_output_path)
        os.remove(self.log_output_path)
        os.remove(self.result_output_path)

if __name__ == '__main__':
    unittest.main()
