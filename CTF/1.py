#Код для перебора чисел от 1 до 10000 на сервере.
import socket
import time

# Настройки подключения
host = "ctf.hackatom.ru"
port = 1234

# Диапазон чисел для перебора
start = 1
end = 100000

# Подключение к серверу и отправка чисел
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Подключено к {host}:{port}")

        for number in range(start, end + 1):

            # Отправка числа в виде строки
            message = f"{number}\n"  # Добавляем перенос строки, если требуется
            s.sendall(message.encode('utf-8'))

            # Получение ответа от сервера
            response = s.recv(1024).decode('utf-8')
            print(f"Отправлено: {number}, Ответ: {response.strip()}")

            # Если сервер вернул специфичный ответ, можно прервать
            if "success" in response.lower():  # Замените "success" на ожидаемую часть ответа
                print(f"Найден ответ: {number}")
                break

except ConnectionError as e:
    print(f"Ошибка подключения: {e}")
