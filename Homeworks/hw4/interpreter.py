import struct
import xml.etree.ElementTree as ET

class VirtualMachine:
    def __init__(self):
        self.stack = []  # Стек для операций
        self.memory = {}  # Память для хранения значений

    def push(self, value):
        """Добавляет значение на вершину стека."""
        self.stack.append(value)

    def pop(self):
        """Снимает значение с вершины стека."""
        if len(self.stack) == 0:
            raise IndexError("Stack underflow")
        return self.stack.pop()

    def execute(self, command):
        """Выполняет одну команду."""
        opcode = command[0]
        if opcode == 0x9A:  # Загрузка константы
            constant = struct.unpack("<I", command[1:5])[0]
            self.push(constant)
        elif opcode == 0xD8:  # Чтение значения из памяти
            address = struct.unpack("<I", command[1:5])[0]
            value = self.memory.get(address, 0)
            self.push(value)
        elif opcode == 0x8E:  # Запись значения в память
            offset = struct.unpack("<I", command[1:5])[0]
            if len(self.stack) < 1:
                raise IndexError("Stack underflow: not enough elements to write to memory.")
            address = self.pop() + offset
            value = self.pop()
            self.memory[address] = value
        elif opcode == 0x4B:  # Бинарная операция (сдвиг влево)
            address2 = struct.unpack("<I", command[1:5])[0]
            if len(self.stack) < 2:
                raise IndexError("Stack underflow: not enough elements for binary operation.")
            address1 = self.pop()
            value1 = self.memory.get(address1, 0)
            value2 = self.memory.get(address2, 0)
            self.push(value1 << value2)
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

def interpret(input_file, output_file, memory_range):
    """
    Читает бинарный файл с командами, выполняет их и сохраняет результаты в XML-файл.

    :param input_file: путь к входному бинарному файлу
    :param output_file: путь к выходному XML-файлу
    :param memory_range: диапазон адресов памяти для записи в XML
    """
    vm = VirtualMachine()

    # Читаем бинарный файл
    with open(input_file, "rb") as binary:
        commands = binary.read()

    # Выполняем команды
    for i in range(0, len(commands), 5):
        command = commands[i:i+5]
        vm.execute(command)

    # Записываем результат памяти в XML
    root = ET.Element("result")
    for addr in range(memory_range[0], memory_range[1]):
        value = vm.memory.get(addr, 0)
        memory_entry = ET.SubElement(root, "memory", address=str(addr))
        memory_entry.text = str(value)

    # Сохраняем XML
    tree = ET.ElementTree(root)
    tree.write(output_file)

if __name__ == "__main__":
    # Пример использования
    interpret("program.bin", "result.xml", (0, 12))
