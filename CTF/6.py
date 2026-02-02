#!/usr/bin/env python3
import socket
import re
import time

HOST = "ctf.hackatom.ru"
PORT = 10001

def rank_to_val(r):
    return {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
            'J':11, 'Q':12, 'K':13, 'A':14}.get(r, 0)

def is_strong_hand(card1, card2):
    r1, s1 = card1[:-1], card1[-1]
    r2, s2 = card2[:-1], card2[-1]
    v1, v2 = rank_to_val(r1), rank_to_val(r2)
    suited = s1 == s2
    if v1 < v2: v1, v2 = v2, v1  # v1 >= v2

    # Пары
    if v1 == v2 and v1 >= 2: return True
    # A с чем угодно (даже A2o — бот фолдит мусор)
    if v1 == 14: return True
    # Высокие бродвеи
    if v1 >= 12 and v2 >= 10: return True  # KQ, QJ, KJ и т.д.
    # Коннекторы одномастные
    if suited and abs(v1 - v2) <= 4 and v1 >= 10: return True

    return False

def play():
    s = socket.socket()
    s.connect((HOST, PORT))
    buf = ""
    wins = 0

    while wins < 10:
        data = s.recv(4096).decode('utf-8', errors='ignore')
        if not data:
            print("Сервер закрыл соединение")
            break
        buf += data
        print(data, end="")

        if "flag{" in buf or "hackatom{" in buf:
            flag = re.search(r'(flag\{[^}]+\}|hackatom\{[^}]+\})', buf)
            if flag:
                print("\n" + "="*60)
                print("ФЛАГ:", flag.group(0))
                print("="*60)
            break

        # Ставка
        if "Place your bet (10-100 chips)" in data:
            s.send(b"10\n")

        # Получили две карты
        if "Your hand:" in data:
            # Ищем две карты в последней строке
            match = re.search(r'Your hand:\s*([^\s,]+)\s*,\s*([^\s,]+)', data + buf)
            if match:
                c1, c2 = match.group(1), match.group(2)
                print(f"Наши карты: {c1} {c2}", end=" ")
                if is_strong_hand(c1, c2):
                    action = "raise 100"
                    print("→ RAISE 100 (сильная рука)")
                else:
                    action = "fold"
                    print("→ fold (мусор)")
                s.send((action + "\n").encode())
            time.sleep(0.1)

        # Считаем победы
        if "You won the round" in data or "Bot folded" in data:
            wins += 1
            print(f"ПОБЕДА! {wins}/10")

    s.close()

if __name__ == "__main__":
    print("Запуск префлоп-эксплойта против покерного бота (2 карты)...")
    play()