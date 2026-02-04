# 🚩 Универсальный поиск флагов

> Сохраните в `~/flags/flag_hunting.md`

---

## 🐧 Linux — где искать флаги

### Универсальная команда (сохраните как алиас!)
```bash
grep -r "RS{" /home /root /opt /var/www /etc /tmp 2>/dev/null | grep -v "proc\|sys\|dev\|run\|bin\|sbin\|lib" | head -40
```

### Поиск по имени файла
```bash
find / -name "*flag*" -o -name "*proof*" -o -name "*key*" 2>/dev/null | head -30
```

### Типичные пути
| Категория | Пути |
|-----------|------|
| **Пользователи** | `/home/*/flag.txt`, `/home/*/.flag`, `/root/flag.txt`, `/root/.flag` |
| **Веб** | `/var/www/html/flag.php`, `/var/www/flag.txt`, `/opt/web/flag` |
| **Система** | `/opt/flag`, `/etc/flag`, `/mnt/flag`, `/srv/flag` |
| **Базы данных** | `mysql -e "SELECT * FROM flags"`, `sqlite3 /opt/app.db "SELECT flag FROM secrets"` |
| **Docker** | `docker ps`, `docker exec <container> grep -r "RS{" /` |

### Неочевидные места (часто упускают!)

```bash
# Переменные окружения
env | grep -iE "flag|secret|key|token"

# История команд
cat ~/.bash_history
cat /home/*/.bash_history 2>/dev/null

# .git/ репозитории
cd /var/www/html && git log --all --oneline --source | head -10
git show <commit_hash> | grep "RS{"

# Метаданные файлов
exiftool /var/www/html/image.jpg | grep "RS{"

# Память процессов
grep -a "RS{" /proc/*/environ 2>/dev/null
strings /proc/kcore | grep "RS{" | head -5

# Cron jobs
cat /etc/cron*/* 2>/dev/null | grep -i flag

# Systemd сервисы
systemctl list-units | grep -i flag
journalctl -u flag-service 2>/dev/null | grep "RS{"
```

---

## 🪟 Windows — где искать флаги

### Универсальный поиск
```powershell
findstr /si "RS{" C:\*.* 2>nul
```

### Поиск по путям
```powershell
dir /s /b C:\flag.txt C:\Users\*\Desktop\flag.txt C:\Users\*\Documents\flag.txt C:\ProgramData\flag.txt 2>nul
```

### Типичные пути
| Категория | Пути |
|-----------|------|
| **Пользователи** | `C:\Users\*\Desktop\flag.txt`, `C:\Users\*\Documents\flag.txt` |
| **Система** | `C:\flag.txt`, `C:\ProgramData\flag.txt`, `C:\Windows\Temp\flag.txt` |
| **Веб** | `C:\inetpub\wwwroot\flag.txt`, `C:\xampp\htdocs\flag.php` |
| **Базы данных** | Проверить через SQL Server Management Studio или `sqlcmd` |

### Неочевидные места

```powershell
# Реестр
reg query HKLM /f "RS{" /t REG_SZ /s
reg query HKCU /f "RS{" /t REG_SZ /s

# Переменные окружения
set | findstr /i "flag\|secret\|key"

# История PowerShell
type C:\Users\*\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt 2>nul | findstr "RS{"

# Файлы подкачки
strings C:\pagefile.sys | findstr "RS{" | findstr /c:"RS{" | head -5

# Браузерные данные (если есть доступ)
dir /s /b C:\Users\*\AppData\Local\Google\Chrome\User Data\Default\History 2>nul
```

---

## 🐳 Docker / контейнеры

```bash
# Проверка запущенных контейнеров
docker ps

# Поиск флагов внутри контейнеров
docker ps -q | xargs -I {} docker exec {} grep -r "RS{" / 2>/dev/null

# Поиск в образах
docker images -q | xargs -I {} docker save {} | strings | grep "RS{" | head -20

# Если вы внутри контейнера — проверка на привилегии
cat /proc/1/cgroup
ls -la /var/run/docker.sock
```

---

## 🌐 Веб-сервисы

| Сервис | Где искать флаги |
|--------|------------------|
| **Grafana** | Дашборды, переменные шаблонов, аннотации |
| **Jenkins** | Логи билдов, переменные окружения, credentials |
| **FreeIPA** | Атрибуты пользователей (`description`, `comment`), группы |
| **Базы данных** | Таблицы `flags`, `secrets`; поля `flag`, `token` |
| **API** | Эндпоинты `/api/flag`, `/api/secrets` |

---

## 🧪 Готовый скрипт поиска (сохраните как `~/flags/find_flag.sh`)

```bash
#!/bin/bash
echo "========================================"
echo " УНИВЕРСАЛЬНЫЙ ПОИСК ФЛАГОВ v1.0"
echo "========================================"

echo "[*] Поиск по содержимому RS{...}"
grep -r "RS{" /home /root /opt /var/www /etc /tmp /mnt 2>/dev/null | grep -v "proc\|sys\|dev\|run\|bin\|sbin\|lib\|usr" | head -40

echo -e "\n[*] Поиск файлов с 'flag' в названии"
find /home /root /opt /var/www /tmp /mnt -name "*flag*" -o -name "*proof*" -o -name "*key*" 2>/dev/null | head -20

echo -e "\n[*] Переменные окружения"
env | grep -iE "flag|secret|key|token" 2>/dev/null

echo -e "\n[*] История команд"
cat ~/.bash_history 2>/dev/null | grep -iE "flag|secret|key" | tail -10
cat /home/*/.bash_history 2>/dev/null | grep -iE "flag|secret|key" | tail -10 2>/dev/null

echo -e "\n[*] .git/ проверка"
if [ -d "/var/www/html/.git" ]; then
  cd /var/www/html && git log --all --oneline --source | head -10
fi

echo "========================================"
echo " ЗАВЕРШЕНО — проверьте вывод выше!"
echo "========================================"
```

Использование:
```bash
chmod +x ~/flags/find_flag.sh
bash ~/flags/find_flag.sh
```
