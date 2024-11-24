# Инициализация векторов
LOAD_CONST 1  # Первый элемент первого вектора
WRITE_MEM 0
LOAD_CONST 2  # Второй элемент первого вектора
WRITE_MEM 1
LOAD_CONST 3  # Третий элемент первого вектора
WRITE_MEM 2
LOAD_CONST 4  # Четвертый элемент первого вектора
WRITE_MEM 3
LOAD_CONST 5  # Пятый элемент первого вектора
WRITE_MEM 4
LOAD_CONST 6  # Шестой элемент первого вектора
WRITE_MEM 5

LOAD_CONST 1  # Первый элемент второго вектора
WRITE_MEM 6
LOAD_CONST 2  # Второй элемент второго вектора
WRITE_MEM 7
LOAD_CONST 3  # Третий элемент второго вектора
WRITE_MEM 8
LOAD_CONST 4  # Четвертый элемент второго вектора
WRITE_MEM 9
LOAD_CONST 5  # Пятый элемент второго вектора
WRITE_MEM 10
LOAD_CONST 6  # Шестой элемент второго вектора
WRITE_MEM 11

# Сдвиг влево и сохранение результата
READ_MEM 0
READ_MEM 6
SHIFT_LEFT 0
WRITE_MEM 0

READ_MEM 1
READ_MEM 7
SHIFT_LEFT 1
WRITE_MEM 1

READ_MEM 2
READ_MEM 8
SHIFT_LEFT 2
WRITE_MEM 2

READ_MEM 3
READ_MEM 9
SHIFT_LEFT 3
WRITE_MEM 3

READ_MEM 4
READ_MEM 10
SHIFT_LEFT 4
WRITE_MEM 4

READ_MEM 5
READ_MEM 11
SHIFT_LEFT 5
WRITE_MEM 5
