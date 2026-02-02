#задача KidsToys
import socket
import time

# Настройки подключения
host = "ctf.hackatom.ru"
port = 1999


# Функция для определения ответа на основе текущей логики
def get_response(color, attempt):
    # Первая логика (1-249 и 500-749)
    if (1 <= attempt <= 250):
        mapping = {
            "green": "yellow",
            "yellow": "blue",
            "blue": "red",
            "red": "green"
        }
    # Вторая логика (250-499)
    elif 251 <= attempt <= 500:
        mapping = {
            "green": "blue",
            "yellow": "blue",
            "blue": "green",
            "red": "red"
        }
    elif 501 <= attempt <= 749:
        mapping = {
            "green": "blue",
            "yellow": "blue",
            "blue": "green",
            "red": "red"
        }
    # Третья логика (750-1000)
    elif 750 <= attempt <= 1000:
        mapping = {
            "green": "blue",
            "yellow": "red",
            "blue": "green",
            "red": "yellow"
        }
    else:
        return "blue"

    return mapping.get(color)


# Подключение к серверу
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print(f"Подключено к {host}:{port}")

    attempt = 1  # Счетчик попыток

    while attempt <= 1001:  # Решить 1000 вопросов
        try:
            # Получение сообщения от сервера
            response = s.recv(1024).decode('utf-8').strip()
            print(f"Сервер: {response}")

            # Если сервер присылает цвет
            if "green" in response or "yellow" in response or "blue" in response or "red" in response:
                # Вычисляем ответ на основе текущей логики
                answer = get_response(response.split()[3], attempt)
                if answer:
                    print(f"Попытка {attempt}: Программа сказала '{response}', я отвечаю '{answer}'")
                    s.sendall(f"{answer}\n".encode('utf-8'))
                else:
                    print("Не удалось определить ответ")

                attempt += 1
            elif "flag" in response.lower():
                print("Флаг получен!")

            else:
                break
        except Exception as e:
            print(f"Ошибка: {e}")
