import pytest
import subprocess
import os
import assembler
import interpreter
import xml.etree.ElementTree as ET

@pytest.fixture(scope="function")
def setup_and_teardown():
    # Путь к файлам
    assembler_path = 'assembler.py'
    interpreter_path = 'interpreter.py'
    test_program_path = 'test_program.asm'
    binary_output_path = 'output.bin'
    log_output_path = 'log.xml'
    result_output_path = 'result.xml'
    
    # Setup code
    yield assembler_path, interpreter_path, test_program_path, binary_output_path, log_output_path, result_output_path
    
    # Teardown code - удаляем файлы только если они существуют
    for file_path in [test_program_path, binary_output_path, log_output_path, result_output_path]:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not remove {file_path}: {e}")


def test_shift_left_vectors(setup_and_teardown):
    assembler_path, interpreter_path, test_program_path, binary_output_path, log_output_path, result_output_path = setup_and_teardown
    
    try:
        # Создание тестовой программы для поэлементного сдвига влево двух векторов длины 6
        with open(test_program_path, 'w') as f:
            # Загружаем значения в память
            for i in range(6):
                f.write(f'LOAD_CONST {i+1}\nWRITE_MEM {i}\n')
            
            # Для каждого элемента: читаем из памяти, загружаем значение сдвига и выполняем сдвиг
            for i in range(6):
                f.write(f'READ_MEM {i}\n')  # Читаем значение
                f.write(f'LOAD_CONST 1\n')   # Загружаем величину сдвига
                f.write(f'SHIFT_LEFT\n')     # Сдвигаем влево
                f.write(f'WRITE_MEM {i}\n')  # Записываем обратно

        # Выводим содержимое тестовой программы
        print("\nTest program content:")
        with open(test_program_path, 'r') as f:
            print(f.read())

        # Запуск ассемблера
        print("\nRunning assembler...")
        result = subprocess.run(
            ['python', assembler_path, test_program_path, binary_output_path, log_output_path],
            capture_output=True,
            text=True,
            check=True
        )
        print("Assembler output:")
        print(result.stdout)
        if result.stderr:
            print("Assembler errors:")
            print(result.stderr)

        # Проверка создания бинарного файла
        if not os.path.exists(binary_output_path):
            raise FileNotFoundError(f"Assembler did not create binary file: {binary_output_path}")
        
        print(f"\nBinary file created: {binary_output_path}")
        print(f"Size: {os.path.getsize(binary_output_path)} bytes")
        
        # Вывод содержимого бинарного файла для отладки
        with open(binary_output_path, 'rb') as f:
            binary_content = f.read()
            print("\nBinary file content (hex):")
            print(' '.join(f'{b:02x}' for b in binary_content))

        # Запуск интерпретатора
        print("\nRunning interpreter...")
        result = subprocess.run(
            ['python', interpreter_path, binary_output_path, result_output_path, '0-5'],
            capture_output=True,
            text=True,
            check=True
        )
        print("Interpreter output:")
        print(result.stdout)
        if result.stderr:
            print("Interpreter errors:")
            print(result.stderr)

        # Проверка результата
        with open(result_output_path, 'r') as f:
            result = f.read()
        print("\nActual XML content:")
        print(result)
        
        # Проверяем, что файл не пустой
        assert result.strip(), "Result file is empty"
        
        for i in range(6):
            expected_value = str((i + 1) << 1)  # Ожидаемое значение после сдвига влево
            expected_pattern = f'<memory address="{i}" value="{expected_value}"'
            print(f"\nLooking for pattern: {expected_pattern}")
            print(f"in result: {result}")
            assert expected_pattern in result, f"Expected pattern not found: {expected_pattern}"
            
    except Exception as e:
        # В случае ошибки выводим больше информации для отладки
        print(f"\nError during test execution: {str(e)}")
        if os.path.exists(binary_output_path):
            print(f"output.bin exists, size: {os.path.getsize(binary_output_path)} bytes")
        else:
            print("output.bin does not exist")
        if os.path.exists(result_output_path):
            print(f"result.xml exists, size: {os.path.getsize(result_output_path)} bytes")
        else:
            print("result.xml does not exist")
        raise


def test_instruction_format(setup_and_teardown):
    assembler_path, interpreter_path, test_program_path, binary_output_path, log_output_path, result_output_path = setup_and_teardown
    try:
        # Создание тестовой программы с примерами команд
        with open(test_program_path, 'w') as f:
            # Загрузка константы (A=154, B=886)
            f.write('LOAD_CONST 886\n')
            
            # Чтение значения из памяти (A=216, B=278)
            f.write('READ_MEM 278\n')
            
            # Запись значения в память (A=142, B=527)
            f.write('WRITE_MEM 527\n')
            
            # Побитовый логический сдвиг влево (A=75, B=683)
            f.write('SHIFT_LEFT 683\n')

        # Запуск ассемблера
        subprocess.run(['python', assembler_path, test_program_path, binary_output_path, log_output_path], check=True)

        # Проверка бинарного файла
        with open(binary_output_path, 'rb') as f:
            binary_data = f.read()

        # Проверка команды LOAD_CONST
        assert binary_data[0:5] == bytes([0x9A, 0x76, 0x03, 0x00, 0x00]), "Неверный формат команды LOAD_CONST"
        
        # Проверка команды READ_MEM
        assert binary_data[5:10] == bytes([0xD8, 0x16, 0x01, 0x00, 0x00]), "Неверный формат команды READ_MEM"
        
        # Проверка команды WRITE_MEM
        assert binary_data[10:15] == bytes([0x8E, 0x0F, 0x02, 0x00, 0x00]), "Неверный формат команды WRITE_MEM"
        
        # Проверка команды SHIFT_LEFT
        assert binary_data[15:20] == bytes([0x4B, 0xAB, 0x02, 0x00, 0x00]), "Неверный формат команды SHIFT_LEFT"

    except Exception as e:
        print(f"\nError during test execution: {str(e)}")
        # Проверяем существование файлов
        if os.path.exists(binary_output_path):
            print(f"output.bin exists, size: {os.path.getsize(binary_output_path)} bytes")
        if os.path.exists(result_output_path):
            print(f"result.xml exists, size: {os.path.getsize(result_output_path)} bytes")
        raise


def test_vector_shift(setup_and_teardown):
    """
    Тест программы vector_shift.asm, которая выполняет поэлементный побитовый сдвиг влево
    над двумя векторами длины 6, записывая результат в первый вектор
    """
    # Путь к тестовым файлам
    asm_file = "vector_shift.asm"
    bin_file = "vector_shift.bin"
    log_file = "vector_shift_log.xml"
    result_file = "vector_shift_result.xml"

    try:
        # Запускаем ассемблер
        subprocess.run(['python', 'assembler.py', asm_file, bin_file, log_file], check=True)
        assert os.path.exists(bin_file), "Бинарный файл не создан"
        
        # Запускаем интерпретатор
        subprocess.run(['python', 'interpreter.py', bin_file, result_file, '0-11'], check=True)
        assert os.path.exists(result_file), "Файл результатов не создан"
        
        # Читаем результаты из XML файла
        tree = ET.parse(result_file)
        root = tree.getroot()
        memory = {}
        for mem_elem in root.findall('.//memory'):
            addr = int(mem_elem.get('address'))
            value = int(mem_elem.get('value'))
            memory[addr] = value
        
        # Проверяем результаты сдвига
        expected_results = {
            0: 10 << 2,  # 40 (сдвиг 10 на 2 позиции)
            1: 20 << 3,  # 160 (сдвиг 20 на 3 позиции)
            2: 30 << 1,  # 60 (сдвиг 30 на 1 позицию)
            3: 40 << 4,  # 640 (сдвиг 40 на 4 позиции)
            4: 50 << 2,  # 200 (сдвиг 50 на 2 позиции)
            5: 60 << 3,  # 480 (сдвиг 60 на 3 позиции)
        }
        
        # Проверяем второй вектор (не должен измениться)
        expected_shifts = {
            6: 2,
            7: 3,
            8: 1,
            9: 4,
            10: 2,
            11: 3
        }
        
        # Проверяем результаты первого вектора
        for addr, expected in expected_results.items():
            assert memory[addr] == expected, f"Неверный результат сдвига в ячейке {addr}: ожидалось {expected}, получено {memory[addr]}"
        
        # Проверяем, что второй вектор не изменился
        for addr, expected in expected_shifts.items():
            assert memory[addr] == expected, f"Второй вектор был изменен в ячейке {addr}: ожидалось {expected}, получено {memory[addr]}"

    except subprocess.CalledProcessError as e:
        print(f"Error during test execution: {e}")
        if os.path.exists(bin_file):
            print(f"{bin_file} exists, size: {os.path.getsize(bin_file)} bytes")
        else:
            print(f"{bin_file} does not exist")
        if os.path.exists(result_file):
            print(f"{result_file} exists, size: {os.path.getsize(result_file)} bytes")
        else:
            print(f"{result_file} does not exist")
        raise

    finally:
        # Очистка тестовых файлов
        for file in [bin_file, log_file, result_file]:
            if os.path.exists(file):
                os.remove(file)
