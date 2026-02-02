#!/usr/bin/env python3
# rainbow100.py — 100 русских цветовых акронимов
# nc ctf.hackatom.ru 1337

import socket
import re
import time

HOST = "ctf.hackatom.ru"
PORT = 1337

# Что начинается на эти буквы → какой цвет
# ИСПРАВЛЕНИЕ: Добавлен префикс "о" для оранжевого цвета.
COLOR_MAP = {
    "кр": "красный",
    "ора": "оранжевый",
    "о": "оранжевый",  # <-- ДОБАВЛЕНО для слов, начинающихся на "О"
    "же": "желтый",
    "зе": "зеленый",
    "го": "голубой",
    "си": "синий",
    "фи": "фиолетовый",
}


def get_color(acronym: str) -> str:
    acronym = acronym.lower()

    # Сортируем ключи по длине в убывающем порядке, чтобы более длинные
    # префиксы (например, "ора") проверялись раньше, чем короткие ("о").
    # Это делает поиск более надежным, хотя в данном случае оба ведут к одному цвету.
    sorted_map = sorted(COLOR_MAP.items(), key=lambda item: len(item[0]), reverse=True)

    for start, color in sorted_map:
        if acronym.startswith(start):
            return color

    # Если не найдено, возвращаем "красный" как запасной вариант (по старому условию)
    return "красный"


def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    buffer = ""
    solved = 0  # Обнуляем счетчик, т.к. при старте он должен быть 0

    while True:
        data = s.recv(4096).decode(errors="ignore")
        if not data:
            print("Сервер закрыл соединение")
            break

        buffer += data

        # Выводим только важное (можно убрать)
        for line in data.splitlines():
            if line.strip():
                print(line)

        # Флаг пришёл → конец
        if "hackatom{" in buffer:
            flag = re.search(r"hackatom\{[^}]+}", buffer)
            print("\n" + "=" * 60)
            print("ФЛАГ:", flag.group(0) if flag else "найден, но не распаршен")
            print("=" * 60)
            break

        # Ошибка → полный рестарт
        if "Прогресс сброшен" in data or "Неправильно" in data:
            print("СБРОС! Начинаем заново...\n")
            solved = 0
            buffer = ""

        # Ищем новую загадку
        # Загадка всегда заканчивается точкой и после неё сразу "Ваш ответ:"
        match = re.search(r"Загадка \d+/100:\s*(.+?)\.\s*Ваш ответ:", buffer, re.DOTALL)
        if not match:
            # иногда точка пропущена — ищем просто до "Ваш ответ:"
            match = re.search(r"Загадка \d+/100:\s*(.+?)\s*Ваш ответ:", buffer, re.DOTALL)

        if match:
            riddle = match.group(1).strip()
            # Берём первые буквы русских слов
            words = re.findall(r'[а-яёА-ЯЁ]+', riddle)
            acronym = "".join(w[0].lower() for w in words)

            answer = get_color(acronym)
            solved += 1
            print(f"[{solved}/100] {riddle}")
            print(f"    Акроним → {acronym} → {answer}\n")

            s.send((answer + "\n").encode())
            time.sleep(1)  # <-- ЗАМЕДЛЕНО до 1 секунды

            # Очищаем буфер, чтобы не обрабатывать одну и ту же загадку дважды
            buffer = buffer[match.end():]

    s.close()


if __name__ == "__main__":
    print("Запускаю решение 100 цветовых загадок...\n")
    main()