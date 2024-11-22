from assembler import assemble
from interpreter import interpret

def create_test_program():
    """
    Создание примерной программы для тестирования.
    """
    with open("program.txt", "w") as program:
        # Пример программы: поэлементный сдвиг двух векторов
        program.write("A=154 B=6\n")  # Длина вектора
        for i in range(6):  # Длина вектора
            program.write(f"A=154 B={i}\n")  # Загрузка первого элемента
            program.write(f"A=154 B={6 + i}\n")  # Загрузка второго элемента
            program.write("A=75 B=0\n")  # Побитовый сдвиг влево
    
    print("Тестовая программа создана: program.txt")

def test_full_pipeline():
    """
    Полный тестовый цикл: ассемблер + интерпретатор.
    """
    create_test_program()                      # Создание программы
    assemble("program.txt", "program.bin", "log.xml")  # Ассемблирование
    interpret("program.bin", "result.xml", (0, 12))    # Интерпретация

if __name__ == "__main__":
    test_full_pipeline()
