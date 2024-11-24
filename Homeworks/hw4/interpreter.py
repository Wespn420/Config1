# Интерпретатор для учебной виртуальной машины (УВМ)

import sys
import xml.etree.ElementTree as ET

# Функция для выполнения команд из бинарного файла

def interpret(binary_file, result_file, memory_range):
    # Инициализация стека и памяти
    stack = []
    memory = [0] * 1024  # Простая модель памяти

    # Чтение бинарного файла
    with open(binary_file, 'rb') as file:
        binary_data = file.read()

    # Обработка каждой команды
    i = 0
    while i < len(binary_data):
        opcode = binary_data[i]
        operand = int.from_bytes(binary_data[i+1:i+5], byteorder='little')
        i += 5

        if opcode == 0x9A:  # LOAD_CONST
            stack.append(operand)
        elif opcode == 0xD8:  # READ_MEM
            stack.append(memory[operand])
        elif opcode == 0x8E:  # WRITE_MEM
            value = stack.pop()
            memory[operand] = value
        elif opcode == 0x4B:  # SHIFT_LEFT
            shift_amount = stack.pop()
            value = stack.pop()
            stack.append(value << shift_amount)
        else:
            raise ValueError(f'Unknown opcode: {opcode}')

    # Запись результатов в XML файл
    root = ET.Element('result')
    for addr in range(memory_range[0], memory_range[1]):
        ET.SubElement(root, 'memory', address=str(addr), value=str(memory[addr]))

    tree = ET.ElementTree(root)
    tree.write(result_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: interpreter.py <binary_file> <result_file> <memory_range>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    memory_range = list(map(int, sys.argv[3].split('-')))

    interpret(binary_file, result_file, memory_range)
