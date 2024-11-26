# Интерпретатор для учебной виртуальной машины (УВМ)

import sys
import xml.etree.ElementTree as ET
import os

# Функция для выполнения команд из бинарного файла

def interpret(binary_file, result_file, memory_range):
    # Инициализация стека и памяти
    stack = []
    memory = [0] * 1024  # Простая модель памяти

    print(f"Opening binary file: {binary_file}")
    # Чтение бинарного файла
    try:
        with open(binary_file, 'rb') as file:
            binary_data = file.read()
            print(f"Read {len(binary_data)} bytes from binary file")
            if len(binary_data) == 0:
                raise ValueError("Binary file is empty")
            if len(binary_data) % 5 != 0:
                raise ValueError(f"Invalid binary file size: {len(binary_data)} bytes (should be multiple of 5)")
    except Exception as e:
        print(f"Error reading binary file: {e}")
        raise

    # Обработка каждой команды
    i = 0
    try:
        while i < len(binary_data):
            opcode = binary_data[i]
            operand = int.from_bytes(binary_data[i+1:i+5], byteorder='little')
            print(f"Processing instruction: opcode={hex(opcode)}, operand={operand}")
            i += 5

            if opcode == 0x9A:  # LOAD_CONST
                stack.append(operand)
                print(f"LOAD_CONST {operand}, stack: {stack}")
            elif opcode == 0xD8:  # READ_MEM
                if operand >= len(memory):
                    raise ValueError(f"Memory address out of bounds: {operand}")
                stack.append(memory[operand])
                print(f"READ_MEM {operand}, value={memory[operand]}, stack: {stack}")
            elif opcode == 0x8E:  # WRITE_MEM
                if not stack:
                    raise ValueError("Stack is empty during WRITE_MEM")
                if operand >= len(memory):
                    raise ValueError(f"Memory address out of bounds: {operand}")
                value = stack.pop()
                memory[operand] = value
                print(f"WRITE_MEM {operand}, value={value}, stack: {stack}")
            elif opcode == 0x4B:  # SHIFT_LEFT
                if not stack:
                    raise ValueError("Stack is empty during SHIFT_LEFT")
                value = stack.pop()
                result = value << 1
                stack.append(result)
                print(f"SHIFT_LEFT: value={value}, shift by 1, result={result}, stack: {stack}")
            else:
                raise ValueError(f'Unknown opcode: {hex(opcode)}')
    except Exception as e:
        print(f"Error during instruction execution: {e}")
        print(f"Current stack state: {stack}")
        print(f"Memory state at addresses {memory_range}: {[memory[i] for i in range(memory_range[0], memory_range[1] + 1)]}")
        raise

    print("\nFinal memory state:")
    start, end = memory_range
    for addr in range(start, end + 1):
        print(f"Memory[{addr}] = {memory[addr]}")

    print(f"\nWriting result to {result_file}")
    # Запись результатов в XML файл
    try:
        root = ET.Element('result')
        for addr in range(start, end + 1):
            mem_elem = ET.SubElement(root, 'memory')
            mem_elem.set('address', str(addr))
            mem_elem.set('value', str(memory[addr]))
            print(f"Creating XML element: <memory address='{addr}' value='{memory[addr]}' />")

        tree = ET.ElementTree(root)
        with open(result_file, 'w', encoding='utf-8') as f:
            tree.write(f, encoding='unicode')
            # Проверяем, что файл не пустой
            f.seek(0, 2)  # Перемещаемся в конец файла
            if f.tell() == 0:
                raise ValueError("Failed to write XML content - file is empty")
        print("Successfully wrote result file")
    except Exception as e:
        print(f"Error writing result file: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: interpreter.py <binary_file> <result_file> <memory_range>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    try:
        # Проверяем существование входного файла
        if not os.path.exists(binary_file):
            print(f"Error: Input file '{binary_file}' does not exist")
            sys.exit(1)

        # Парсим диапазон памяти из строки вида "0-5"
        try:
            start, end = map(int, sys.argv[3].split('-'))
            memory_range = [start, end]
        except ValueError:
            print(f"Error: Invalid memory range format. Expected 'start-end', got '{sys.argv[3]}'")
            sys.exit(1)

        # Запускаем интерпретатор
        try:
            interpret(binary_file, result_file, memory_range)
        except Exception as e:
            print(f"Error during interpretation: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
