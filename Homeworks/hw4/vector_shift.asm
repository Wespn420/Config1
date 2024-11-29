# Первый вектор (записываем в ячейки 0-5)
LOAD_CONST 10
WRITE_MEM 0
LOAD_CONST 20
WRITE_MEM 1
LOAD_CONST 30
WRITE_MEM 2
LOAD_CONST 40
WRITE_MEM 3
LOAD_CONST 50
WRITE_MEM 4
LOAD_CONST 60
WRITE_MEM 5

# Второй вектор (записываем в ячейки 6-11)
LOAD_CONST 2
WRITE_MEM 6
LOAD_CONST 3
WRITE_MEM 7
LOAD_CONST 1
WRITE_MEM 8
LOAD_CONST 4
WRITE_MEM 9
LOAD_CONST 2
WRITE_MEM 10
LOAD_CONST 3
WRITE_MEM 11

# Выполняем сдвиг влево для каждого элемента первого вектора
# на количество позиций из соответствующего элемента второго вектора
READ_MEM 0    # Читаем элемент из первого вектора
READ_MEM 6    # Читаем соответствующий элемент из второго вектора
SHIFT_LEFT    # Выполняем сдвиг
WRITE_MEM 0   # Записываем результат обратно в первый вектор

READ_MEM 1
READ_MEM 7
SHIFT_LEFT
WRITE_MEM 1

READ_MEM 2
READ_MEM 8
SHIFT_LEFT
WRITE_MEM 2

READ_MEM 3
READ_MEM 9
SHIFT_LEFT
WRITE_MEM 3

READ_MEM 4
READ_MEM 10
SHIFT_LEFT
WRITE_MEM 4

READ_MEM 5
READ_MEM 11
SHIFT_LEFT
WRITE_MEM 5
