import unittest
import os
import tempfile
from zipfile import ZipFile
from Emulator import ZipEmulator  # Импортируем эмулятор из основной программы

class TestZipEmulator(unittest.TestCase):

    def setUp(self):
        # Создаем временный zip-файл для каждого теста
        self.temp_dir = tempfile.TemporaryDirectory()
        self.zip_file_path = os.path.join(self.temp_dir.name, "test_files.zip")
        with ZipFile(self.zip_file_path, 'w') as myzip:
            pass

        # Экземпляр эмулятора с временным zip-файлом
        self.emulator = ZipEmulator(self.zip_file_path)

    def test_ls_empty_directory(self):
        # Тест команды ls в пустом архиве
        output = self.emulator.run("ls")
        self.assertEqual(output, [""])

    def test_ls_after_touch(self):
        # Тест команды ls после создания файла
        self.emulator.run("touch file1.txt")
        output = self.emulator.run("ls")
        self.assertIn("file1.txt", output[0])

    def test_cd_and_ls(self):
        # Тест перехода в подкаталог и команды ls
        self.emulator.run("touch folder1/file2.txt")
        self.emulator.run("cd folder1")
        output = self.emulator.run("ls")
        self.assertIn("file2.txt", output[0])

    def test_cd_nonexistent_directory(self):
        # Тест попытки перехода в несуществующий каталог
        self.emulator.run("cd nonexistent")
        output = self.emulator.run("ls")
        self.assertEqual(output, [""])  # Пустая директория, т.к. переход не удался

    def test_touch_creates_file(self):
        # Тест создания файла с помощью команды touch
        self.emulator.run("touch newfile.txt")
        output = self.emulator.run("ls")
        self.assertIn("newfile.txt", output[0])

    def test_touch_existing_file(self):
        # Тест, для создания уже существующего файла
        self.emulator.run("touch existingfile.txt")
        output1 = self.emulator.run("ls")
        self.assertIn("existingfile.txt", output1[0])
        
        output2 = self.emulator.run("touch existingfile.txt")
        self.assertIn("Файл existingfile.txt уже существует.", output2)

    def test_find_existing_file(self):
        # Тест команды find для существующего файла
        self.emulator.run("touch folder1/file3.txt")
        output = self.emulator.run("find file3.txt")
        self.assertIn("folder1/file3.txt", output[0])

    def test_find_nonexistent_file(self):
        # Тест команды find для несуществующего файла
        output = self.emulator.run("find missing.txt")
        self.assertIn("Файл missing.txt не найден.", output[0])

if __name__ == '__main__':
    unittest.main()
