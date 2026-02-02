#задание с архивами
import base64
import os
import patoolib

output_dir = "output"
temp_dir = output_dir + "/temp"
current_archive = "archive.rar"


def extract_archive_with_password(archive_path, password, output_folder):
    """
    Извлекает архив с заданным паролем.
    """
    try:
        if not password:
            patoolib.extract_archive(archive_path, outdir=output_folder)
            print(f"Архив {archive_path} успешно извлечен без использования пароля")
            return True
        patoolib.extract_archive(archive_path, outdir=output_folder, password=password)
        print(f"Архив {archive_path} успешно извлечен с использованием пароля: {password}")
        return True
    except Exception as e:
        print(f"Ошибка при извлечении {archive_path}: {e}")
        return False

def decode_password_from_txt(path_to_txt):
    """
    Декодирует пароль из текстового файла.
    """
    with open(path_to_txt, "r") as f:
        encoded_password = f.read().strip()
        password = base64.b64decode(encoded_password).decode()
        print(f"Декодированный пароль: {password}")
        return str(password)


if __name__ == "__main__":
    # Создаем выходную папку
    os.makedirs(temp_dir, exist_ok=True)
    # Извлекаем начальный архив
    extract_success = extract_archive_with_password(current_archive, None, temp_dir)

    current_archive = [f"{temp_dir}/{item}" for item in os.listdir(temp_dir) if item.endswith(".rar")][0]

    while current_archive:
        # Открываем текущий архив
        print(f"Обработка архива: {current_archive}")

        # Декодируем пароль
        password = decode_password_from_txt(f"{temp_dir}/README.txt")
        os.remove(f"{temp_dir}/README.txt")
        if not password:
            print("Пароль не найден! Остановка.")
            break

        # Распаковываем текущий архив с паролем
        extract_success = extract_archive_with_password(current_archive, password, temp_dir)
        os.remove(f"{current_archive}")
        if not extract_success:
            print(f"Не удалось распаковать архив {current_archive}. Остановка.")
            break

        # Ищем следующий архив
        try:
            current_archive = [f"{temp_dir}/{item}" for item in os.listdir(temp_dir) if item.endswith(".rar")][0]
        except IndexError:
            current_archive = None
