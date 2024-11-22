import struct

def assemble(input_file, output_file):
    """
    Ассемблер для УВМ.
    Преобразует текстовый файл команд в бинарный файл.
    """
    with open(input_file, 'r') as source, open(output_file, 'wb') as binary:
        for line in source:
            line = line.strip()
            if not line or '=' not in line:
                continue

            # Разбираем строку вида: "A=154 B=886"
            parts = line.split()
            try:
                a = int(parts[0].split('=')[1])  # Читаем A
                b = int(parts[1].split('=')[1])  # Читаем B
            except (IndexError, ValueError):
                print(f"Ошибка обработки строки: '{line}'")
                continue

            # Преобразование в бинарную команду: A (1 байт) + B (4 байта)
            command = struct.pack("<BI", a, b)
            binary.write(command)  # Запись в бинарный файл

if __name__ == "__main__":
    assemble("program.txt", "program.bin")
