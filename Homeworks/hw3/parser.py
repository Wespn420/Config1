import sys
import re
import toml


def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("'") or line.startswith("#"):
            continue  # Пропускаем пустые строки и комментарии

        # Обработка синтаксиса: <function>(...) -> имя;
        match = re.match(r'([\w]+)\((.+)\)\s*->\s*(\w+);', line)
        if match:
            func, content, name = match.groups()
            if func == 'pow':
                # Evaluate power function
                base, exp = map(int, content.split(','))
                data[name] = pow(base, exp)
            else:
                # Interpret any other function call as an array
                data[name] = parse_array(content, data)
            continue

        # Обработка выражений: {выражение} -> имя;
        match = re.match(r'\{(.+)\}\s*->\s*(\w+);', line)
        if match:
            expr, name = match.groups()
            data[name] = eval_constant_expression("{" + expr + "}", data)
            continue

        # Обработка констант: значение -> имя;
        match = re.match(r'(\d+)\s*->\s*(\w+);', line)
        if match:
            value, name = match.groups()
            data[name] = int(value)
            continue

        # Вывод ошибок для неподдерживаемого синтаксиса
        raise SyntaxError(f"Syntax error: {line}")

    return data


def eval_expression(expr, data):
    """Оценивает значение выражения или возвращает ссылку на данные."""
    if expr.isdigit():
        return int(expr)
    elif expr.startswith("'") and expr.endswith("'"):
        # Возвращаем строку как есть, без добавления дополнительных кавычек
        return expr
    elif expr.startswith("{") and expr.endswith("}"):
        return eval_constant_expression(expr, data)
    elif "(" in expr and ")" in expr:  # Обрабатываем вложенные массивы
        func_name = expr[:expr.index("(")]
        if func_name == "pow":
            args = expr[expr.index("(")+1:expr.index(")")].split(",")
            return pow(int(args[0]), int(args[1]))
        else:
            content = expr[expr.index("(")+1:expr.index(")")]
            return parse_array(content, data)
    return data.get(expr, expr)  # Ссылка на ранее определенные данные или значение


def parse_array(content, data):
    """Парсинг содержимого массива, включая вложенные структуры."""
    content = content.strip()  # Remove leading/trailing whitespace
    elements = split_array_elements(content)
    result = []
    for element in elements:
        element = element.strip()
        # Обрабатываем все элементы одинаково
        result.append(eval_expression(element, data))
    return result


def split_array_elements(array_content):
    """Разделяет элементы массива, учитывая вложенные структуры."""
    elements = []
    current = ""
    nesting = 0
    
    for char in array_content:
        if char in '({[':  # Handle nested structures
            nesting += 1
            current += char
        elif char in ')}]':
            nesting -= 1
            current += char
        elif char == ',' and nesting == 0:  # Split only at top-level commas
            elements.append(current.strip())
            current = ""
        else:
            current += char
    
    if current:  # Add the last element
        elements.append(current.strip())
    
    return elements


def eval_constant_expression(expr, data):
    """Вычисляет значения выражений, поддерживает арифметические операции."""
    expr = expr[1:-1]  # Удаляем { и }
    tokens = re.split(r'(\s+|\+|\-|\*|/|\(|\)|,)', expr)
    tokens = [t.strip() for t in tokens if t.strip()]

    # Замена имен на их значения
    for i, token in enumerate(tokens):
        if token in data:
            tokens[i] = str(data[token])
        elif token.isdigit():
            tokens[i] = str(token)

    # Преобразование в строку для eval
    expr_eval = " ".join(tokens)
    try:
        return eval(expr_eval, {"__builtins__": None}, {"pow": pow, "mod": lambda x, y: x % y})
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {e}")


def write_toml(data, output_path):
    """Записывает данные в TOML файл."""
    print(f"Writing data to {output_path}:")
    print("Data to write:", data)
    try:
        with open(output_path, 'w') as file:
            toml.dump(data, file)
        print(f"Successfully wrote to {output_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python parser.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        print(f"Parsing file: {input_file}")
        data = parse_file(input_file)
        print("Parsed data:", data)
        write_toml(data, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
