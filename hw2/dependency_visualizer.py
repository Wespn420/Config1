import subprocess
import os
from pathlib import Path

def get_git_commits(repo_path):
    """
    Возвращает словарь коммитов и их зависимостей для указанного git-репозитория.
    Ключ - хеш коммита, значение - список хешей родительских коммитов.
    """
    result = subprocess.run(['git', '-C', repo_path, 'log', '--pretty=format:%H %P'], 
                            capture_output=True, text=True, check=True)
    commits = {}
    for line in result.stdout.strip().split('\n'):
        parts = line.split()
        commit_hash = parts[0]
        parent_hashes = parts[1:]
        commits[commit_hash] = parent_hashes
    return commits

def generate_dot_graph(commits):
    """
    Генерирует описание графа в формате DOT для переданного словаря коммитов.
    """
    lines = ['digraph G {']
    for commit, parents in commits.items():
        for parent in parents:
            lines.append(f'    "{parent}" -> "{commit}";')
    lines.append('}')
    return '\n'.join(lines)

def save_graph_to_file(dot_graph, output_path, graphviz_path):
    """
    Сохраняет граф в файл PNG, используя Graphviz.
    """
    dot_file = Path(output_path).with_suffix('.dot')
    with open(dot_file, 'w') as file:
        file.write(dot_graph)
    
    # Вызываем Graphviz для создания PNG из DOT-файла
    subprocess.run([graphviz_path, '-Tpng', dot_file.as_posix(), '-o', Path(output_path).as_posix()], check=True)
    print(f"Граф успешно сохранен в {output_path}")
