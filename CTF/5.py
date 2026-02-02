import DNS
from scapy.all import *


def rdpcap(param):
    pass


packets = rdpcap("capture.pcap")

# Словарь: поддомен → следующий поддомен (по CNAME)
cname_chain = {}
# Словарь: поддомен → TXT-запись
txt_data = {}

for p in packets:
    if p.haslayer(DNS) and p[DNS].qr == 1:  # ответы
        if hasattr(p[DNS], 'an') and p[DNS].an:
            for i in range(p[DNS].ancount):
                rr = p[DNS].an[i]
                name = rr.rrname.decode().lower()
                if b"maze.rctf2021.xctf.org.cn" in name:
                    if rr.type == 5:  # CNAME
                        next_domain = rr.rdata.decode().lower().rstrip(".")
                        cname_chain[name.rstrip(".")] = next_domain
                    elif rr.type == 16:  # TXT
                        txt = rr.rdata[1:] if isinstance(rr.rdata, bytes) else rr.rdata
                        txt_data[name.rstrip(".")] = "".join(txt.decode().split())

# Находим стартовый домен (тот, на который нет входящих CNAME)
all_targets = set(cname_chain.values())
all_sources = set(cname_chain.keys())
start = (all_sources - all_targets).pop()

# Идём по цепочке и собираем TXT
current = start
payload_parts = []

while current in cname_chain:
    if current in txt_data:
        payload_parts.append(txt_data[current])
    current = cname_chain[current]

# Последний TXT тоже нужен
if current in txt_data:
    payload_parts.append(txt_data[current])

full_b64 = "".join(payload_parts)
print(f"Длина base64 строки: {len(full_b64)}")
open("payload.b64", "w").write(full_b64)