import toml
import os
from zipfile import ZipFile, ZipInfo

class ZipEmulator:
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.path = []

    def get_current_path(self):
        return "/".join(self.path) + "/"

    def run(self, command):
        output = []

        with ZipFile(self.zip_file, 'a') as myzip:
            if command == "ls":
                current_dir_files = []
                for name in myzip.namelist():
                    np = name.strip('/').split('/')
                    last = np.pop()
                    if self.path == np:
                        current_dir_files.append(last)
                output.append("  ".join(current_dir_files))

            elif command.startswith("cd "):
                parts = command.split(" ")
                new_path = parts[1].split("/")
                self.path = [i for i in new_path if i != ""]

            elif command.startswith("touch "):
                parts = command.split(" ")
                filename = parts[1]
                file_path = self.get_current_path() + filename
                if file_path not in myzip.namelist():
                    info = ZipInfo(file_path)
                    myzip.writestr(info, "")
                else:
                    output.append(f"Файл {filename} уже существует.")

            elif command.startswith("find "):
                parts = command.split(" ")
                filename = parts[1]
                found_files = []
                found = False
                for name in myzip.namelist():
                    if name.endswith(filename):
                        found_files.append(name)
                        found = True
                if not found:
                    output.append(f"Файл {filename} не найден.")
                else:
                    output.append("\n".join(found_files))

        return output

    def exit(self):
        return "exit"

# Чтение конфигурационного файла
def load_config(config_file="config.toml"):
    try:
        config = toml.load(config_file)
        settings = config['settings']
        computer_name = settings['computer_name']
        zip_file_path = settings['zip_file']
        startup_script = settings.get('startup_script')
        return computer_name, zip_file_path, startup_script
    except (FileNotFoundError, KeyError) as e:
        print(f"Ошибка при чтении конфигурации: {e}")
        return None, None, None

# Выполнение стартового скрипта
def execute_startup_script(startup_script):
    if startup_script and os.path.isfile(startup_script):
        print(f"Выполнение стартового скрипта: {startup_script}")
        os.system(f"bash {startup_script}")
    else:
        print("Стартовый скрипт не найден или не указан.")

# Основной цикл программы
if __name__ == "__main__":
    # Загружаем параметры из конфигурационного файла
    default_computer_name, zip_file_path, startup_script = load_config()

    if not zip_file_path:
        print("Ошибка загрузки конфигурационного файла. Завершение работы.")
    else:
        # Выполняем стартовый скрипт, если он есть
        execute_startup_script(startup_script)

        # Запрашиваем у пользователя имя компьютера
        computer_name = input(f"Введите имя компьютера (по умолчанию: {default_computer_name}): ")

        # Если пользователь не ввел имя, используем значение по умолчанию
        if not computer_name.strip():
            computer_name = default_computer_name

        emulator = ZipEmulator(zip_file_path)

        while True:
            # Ввод команды с отображением имени компьютера
            command = input(f"{computer_name}$ ")  # Имя компьютера в приглашении
            if command == "exit":
                print("Завершение работы.")
                break

            result = emulator.run(command)
            if result:
                print("\n".join(result))
