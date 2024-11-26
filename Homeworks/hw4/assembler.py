import sys
import xml.etree.ElementTree as ET

# Функция для чтения входного файла с программой на ассемблере
# и преобразования инструкций в бинарный формат

def assemble(input_file, binary_file, log_file):
    # Открываем входной файл и читаем все строки
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Инициализируем массив для хранения бинарных данных и логов
    binary_data = bytearray()
    log_entries = []

    # Обрабатываем каждую строку входного файла
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Разбор строки с инструкцией
        parts = line.split()
        command = parts[0]
        operand = int(parts[1]) if len(parts) > 1 else 0

        # Обработка инструкций
        if command == 'LOAD_CONST':
            # Загрузка константы в регистр
            binary_data.extend([0x9A] + list(operand.to_bytes(4, byteorder='little')))
            log_entries.append({'command': command, 'operand': operand})
        elif command == 'READ_MEM':
            # Чтение данных из памяти
            binary_data.extend([0xD8] + list(operand.to_bytes(4, byteorder='little')))
            log_entries.append({'command': command, 'operand': operand})
        elif command == 'WRITE_MEM':
            # Запись данных в память
            binary_data.extend([0x8E] + list(operand.to_bytes(4, byteorder='little')))
            log_entries.append({'command': command, 'operand': operand})
        elif command == 'SHIFT_LEFT':
            # Сдвиг влево
            binary_data.extend([0x4B] + list(operand.to_bytes(4, byteorder='little')))
            log_entries.append({'command': command, 'operand': operand})
        else:
            # Обработка неизвестной инструкции
            raise ValueError(f'Unknown command: {command}')

    # Запись бинарных данных в файл
    with open(binary_file, 'wb') as bin_file:
        bin_file.write(binary_data)

    # Запись лога в XML файл
    root = ET.Element('log')
    for entry in log_entries:
        instruction = ET.SubElement(root, 'instruction')
        for key, value in entry.items():
            instruction.set(key, str(value))

    tree = ET.ElementTree(root)
    with open(log_file, 'w', encoding='utf-8') as f:
        tree.write(f, encoding='unicode', xml_declaration=True)

def check_binary(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        hex_content = ' '.join(f'0x{b:02X}' for b in content)
        print(hex_content)

if __name__ == "__main__":
    # Проверка количества аргументов командной строки
    if len(sys.argv) != 4:
        print("Usage: assembler.py <input_file> <binary_file> <log_file>")
        sys.exit(1)

    # Получение аргументов командной строки
    input_file = sys.argv[1]
    binary_file = sys.argv[2]
    log_file = sys.argv[3]

    # Вызов функции ассемблирования
    assemble(input_file, binary_file, log_file)

    # Проверка бинарного файла
    check_binary(binary_file)
