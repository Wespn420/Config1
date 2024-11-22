import sys
import re
import toml


def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("'"):
            continue  # Пропускаем пустые строки и комментарии

        # Обработка синтаксиса: <function>(...) -> имя;
        match = re.match(r'([\w]+)\((.+)\)\s*->\s*(\w+);', line)
        if match:
            func, content, name = match.groups()
            # Любой вызов функции интерпретируем как массив
            data[name] = parse_array(content, data)
            continue

        # Обработка выражений: {выражение} -> имя;
        match = re.match(r'\{(.+)\}\s*->\s*(\w+);', line)
        if match:
            expr, name = match.groups()
            data[name] = eval_constant_expression("{" + expr + "}", data)
            continue

        # Вывод ошибок для неподдерживаемого синтаксиса
        print(f"Syntax error: {line}")

    return data


def eval_expression(expr, data):
    """Оценивает значение выражения или возвращает ссылку на данные."""
    if expr.isdigit():
        return int(expr)
    elif expr.startswith('"') and expr.endswith('"'):
        return expr.strip('"')
    elif expr.startswith("{") and expr.endswith("}"):
        return eval_constant_expression(expr, data)
    elif "(" in expr and ")" in expr:  # Обрабатываем вложенные массивы
        return parse_array(expr[expr.index("(") + 1 : expr.rindex(")")], data)
    else:
        return data.get(expr, expr)  # Ссылка на ранее определенные данные или значение


def parse_array(content, data):
    """Парсинг содержимого массива, включая вложенные структуры."""
    elements = split_array_elements(content)
    return [eval_expression(element, data) for element in elements]


def split_array_elements(array_content):
    """Разделяет элементы массива, учитывая вложенные структуры."""
    elements = []
    buffer = ""
    depth = 0

    for char in array_content:
        if char == ',' and depth == 0:
            elements.append(buffer.strip())
            buffer = ""
        else:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            buffer += char

    if buffer.strip():
        elements.append(buffer.strip())

    return elements


def eval_constant_expression(expr, data):
    """Вычисляет значения выражений, поддерживает арифметические операции."""
    expr = expr[1:-1]  # Удаляем { и }
    tokens = re.split(r'(\s+|\+|\-|\*|/|pow|mod|\(|\))', expr)
    tokens = [t.strip() for t in tokens if t.strip()]

    # Замена имен на их значения
    for i, token in enumerate(tokens):
        if token in data:
            tokens[i] = str(data[token])

    # Преобразование в строку для eval
    expr_eval = " ".join(tokens)
    try:
        return eval(expr_eval, {"__builtins__": None}, {"pow": pow, "mod": lambda x, y: x % y})
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {e}")


def write_toml(data, output_path):
    with open(output_path, 'w') as file:
        toml.dump(data, file)


def main():
    if len(sys.argv) != 3:
        print("Usage: python parser.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = parse_file(input_file)
    write_toml(data, output_file)


if __name__ == "__main__":
    main()
