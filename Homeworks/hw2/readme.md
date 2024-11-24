# Задание 2

Визуализатор графа зависимостей Git

Этот проект представляет собой инструмент командной строки для визуализации графа зависимостей коммитов в репозитории Git. Инструмент использует Graphviz для генерации графа.

## Установка

Убедитесь, что у вас установлен Python 3.x.

Установите необходимые зависимости:
```
pip install graphviz
```

## Использование

Команда запуска

Для запуска инструмента используйте следующую команду:
```
python git_dependency_graph.py -r <путь_к_репозиторию> -o <выходной_файл> -g <путь_к_graphviz>
```

### Пример команды
```
python git_dependency_graph.py -r C:\path\to\repo -o C:\path\to\output_graph.png -g "C:\Program Files\Graphviz"
```

### Аргументы командной строки

- `<путь_к_репозиторию>`: Путь к анализируемому репозиторию Git.
- `<выходной_файл>`: Путь к файлу-результату в формате PNG.
- `<путь_к_graphviz>`: Путь к программе для визуализации графов (например, "C:\Program Files\Graphviz").

## Пример использования

Запустите скрипт с использованием параметров:
```
python git_dependency_graph.py -r C:\path\to\repo -o C:\path\to\output_graph.png -g "C:\Program Files\Graphviz"
```

## Тестирование

Для запуска тестов используйте следующую команду:
```
python -m unittest test_git_dependency_graph.py
```

## ПОЛУЧИВШИЙСЯ ГРАФ
![output_graph png](https://github.com/user-attachments/assets/c8dd7543-9666-45f6-a942-2fd33bfe10e4)
