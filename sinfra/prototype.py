#!/usr/bin/env python3
"""
Traffic-per-device monitor usando Scapy.

O script:
- captura pacotes na interface (modo promiscuous)
- agrega bytes por IP e MAC (sent / recv)
- conta protocolos por dispositivo (TCP, UDP, ICMP, ARP)
- tenta mapear protocolos de aplicação por porta (HTTP, HTTPS, DNS, SSH, etc.)
- imprime um relatório no terminal a cada INTERVAL segundos

Requisitos:
- scapy (pip install scapy)
- rodar como root/Administrador
"""

import time
import threading
from collections import defaultdict, Counter
from scapy.all import sniff, Ether, IP, TCP, UDP, ICMP, ARP, Raw
import argparse
import signal
import sys

# --------------------
# Configurações
INTERVAL = 5  # segundos entre relatórios
MAX_TABLE_ROWS = 200  # limite para evitar prints enormes
# mapear portas conhecidas para protocolos de aplicação
PORT_PROTO = {
    80: "HTTP",
    443: "HTTPS",
    53: "DNS",
    67: "DHCP/BOOTP",
    68: "DHCP/BOOTP",
    22: "SSH",
    21: "FTP",      # FTP controle
    20: "FTP-DATA", # FTP data (legacy)
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    123: "NTP",
    69: "TFTP",
    3306: "MySQL",
    5432: "Postgres",
    5060: "SIP",
    5061: "SIPS",
    3389: "RDP",
}

# --------------------
# Estruturas globais (thread-safe com locks)
bytes_sent = defaultdict(int)    # key: (ip, mac) -> bytes enviado (onde ip é src)
bytes_recv = defaultdict(int)    # key: (ip, mac) -> bytes recebido (where ip is dst)
protocol_counts = defaultdict(Counter)  # key -> Counter of protocol names
ip_mac_map = {}  # ip -> mac (last seen)
_lock = threading.Lock()

running = True

# --------------------
# Helpers
def key_from_pkt(ip, mac):
    """Retorna tupla chave para armazenar dados."""
    return (ip, mac)

def map_port_to_proto(port):
    return PORT_PROTO.get(port, str(port))

# heurísticas simples para detectar HTTP/FTP pelo payload
def detect_app_by_payload(payload_bytes):
    """Retorna 'HTTP' / 'FTP' / None se detectar padrões no payload."""
    if not payload_bytes:
        return None
    # normalizar início (bytes)
    start = payload_bytes[:16].upper() if len(payload_bytes) >= 16 else payload_bytes.upper()
    # HTTP requests/responses: "GET ", "POST ", "HEAD ", "HTTP/"
    http_signs = [b"GET ", b"POST ", b"HEAD ", b"PUT ", b"DELETE ", b"OPTIONS ", b"HTTP/"]
    for s in http_signs:
        if s in start or payload_bytes.upper().find(s) != -1:
            return "HTTP"
    # FTP control messages: "USER ", "PASS ", "220 ", "230 ", "530 "
    ftp_signs = [b"USER ", b"PASS ", b"220 ", b"230 ", b"530 ", b"331 "]
    for s in ftp_signs:
        if s in start or payload_bytes.upper().find(s) != -1:
            return "FTP"
    return None

def process_packet(pkt):
    try:
        with _lock:
            # lidar com ARP (sem camada IP)
            if ARP in pkt:
                arp = pkt[ARP]
                # ARP tem fields: psrc, pdst, hwsrc, hwdst
                if hasattr(arp, "psrc"):
                    ip = arp.psrc
                    mac = arp.hwsrc
                    ip_mac_map[ip] = mac
                    key = key_from_pkt(ip, mac)
                    protocol_counts[key].update(["ARP"])
                return

            if Ether not in pkt:
                return

            eth = pkt[Ether]
            src_mac = eth.src
            dst_mac = eth.dst

            if IP in pkt:
                ip = pkt[IP]
                src_ip = ip.src
                dst_ip = ip.dst
                size = len(pkt)  # tamanho em bytes

                # atualizar mapa ip->mac (pode não ser perfeito, mas ajuda)
                if src_mac and src_ip:
                    ip_mac_map[src_ip] = src_mac
                if dst_mac and dst_ip:
                    ip_mac_map[dst_ip] = dst_mac

                # keys
                key_src = key_from_pkt(src_ip, ip_mac_map.get(src_ip, src_mac))
                key_dst = key_from_pkt(dst_ip, ip_mac_map.get(dst_ip, dst_mac))

                # atualizar bytes enviados/recebidos
                bytes_sent[key_src] += size
                bytes_recv[key_dst] += size

                # protocolos
                if TCP in pkt:
                    tcp = pkt[TCP]
                    sport = tcp.sport
                    dport = tcp.dport
                    # marca TCP e porta de aplicação se conhecida
                    protocol_counts[key_src].update(["TCP"])
                    protocol_counts[key_dst].update(["TCP"])
                    # aplicações por porta
                    protocol_counts[key_src].update([map_port_to_proto(dport)])
                    protocol_counts[key_dst].update([map_port_to_proto(sport)])

                    # tentar detectar HTTP / FTP inspecionando payload Raw
                    payload = b""
                    if Raw in pkt:
                        try:
                            payload = bytes(pkt[Raw].load)
                        except Exception:
                            payload = b""
                    # heurística por conteúdo do payload
                    app_by_payload = detect_app_by_payload(payload)
                    if app_by_payload == "HTTP":
                        # preferir marcar quem enviou o request (src)
                        protocol_counts[key_src].update(["HTTP"])
                    elif app_by_payload == "FTP":
                        protocol_counts[key_src].update(["FTP"])

                    # reforçar detecção por porta (caso payload vazio)
                    if dport == 80 or sport == 80:
                        protocol_counts[key_src].update(["HTTP"])
                        protocol_counts[key_dst].update(["HTTP"])
                    if dport == 21 or sport == 21 or dport == 20 or sport == 20:
                        protocol_counts[key_src].update(["FTP"])
                        protocol_counts[key_dst].update(["FTP"])

                elif UDP in pkt:
                    udp = pkt[UDP]
                    sport = udp.sport
                    dport = udp.dport
                    protocol_counts[key_src].update(["UDP"])
                    protocol_counts[key_dst].update(["UDP"])
                    protocol_counts[key_src].update([map_port_to_proto(dport)])
                    protocol_counts[key_dst].update([map_port_to_proto(sport)])
                elif ICMP in pkt:
                    protocol_counts[key_src].update(["ICMP"])
                    protocol_counts[key_dst].update(["ICMP"])
                else:
                    # outro protocolo IP — marque com protocolo do IP
                    protocol_counts[key_src].update([f"IP/{ip.proto}"])
                    protocol_counts[key_dst].update([f"IP/{ip.proto}"])
            else:
                # sem IP (p.ex. 802.1Q ou outros) — contar por MAC
                size = len(pkt)
                key = key_from_pkt("unknown", src_mac)
                bytes_sent[key] += size
                protocol_counts[key].update(["NON-IP"])
    except Exception:
        # não interromper sniff por exceção
        return

# --------------------
# Relatório periódico
def human_readable_rate(bytes_count, interval):
    """Retorna string com Kbps/Mbps baseado em bytes e intervalo em segundos."""
    if interval <= 0:
        return "0 bps"
    bits_per_sec = (bytes_count * 8) / interval
    if bits_per_sec >= 1_000_000:
        return f"{bits_per_sec/1_000_000:.2f} Mbps"
    elif bits_per_sec >= 1_000:
        return f"{bits_per_sec/1_000:.2f} Kbps"
    else:
        return f"{bits_per_sec:.2f} bps"

def print_report(interval):
    global bytes_sent, bytes_recv, protocol_counts, ip_mac_map
    while running:
        time.sleep(interval)
        with _lock:
            print("\n" + "="*100)
            print(f"Relatório de tráfego por dispositivo — janela: {interval} s — {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-"*100)
            # coletar todas as chaves conhecidas
            keys = set(bytes_sent.keys()) | set(bytes_recv.keys()) | set(protocol_counts.keys())
            # ordenar por bytes totais decrescentes
            def total_bytes(k):
                return bytes_sent.get(k, 0) + bytes_recv.get(k, 0)
            sorted_keys = sorted(keys, key=total_bytes, reverse=True)[:MAX_TABLE_ROWS]

            if not sorted_keys:
                print("Nenhum tráfego capturado ainda...")
            else:
                # Cabeçalho
                print(f"{'IP':<18} {'MAC':<20} {'Up':>12} {'Down':>12} {'Total':>12}  Protocols (top)")
                print("-"*100)
                for k in sorted_keys:
                    ip, mac = k
                    up_b = bytes_sent.get(k, 0)
                    down_b = bytes_recv.get(k, 0)
                    total_b = up_b + down_b
                    up_str = human_readable_rate(up_b, interval)
                    down_str = human_readable_rate(down_b, interval)
                    total_str = human_readable_rate(total_b, interval)
                    prot_counter = protocol_counts.get(k, Counter())
                    # top 5 protocols
                    top_protocols = ", ".join([f"{p}({c})" for p, c in prot_counter.most_common(5)])
                    print(f"{ip:<18} {mac:<20} {up_str:>12} {down_str:>12} {total_str:>12}  {top_protocols}")
            print("="*100)
            # reset counters (janela deslizante por intervalo)
            bytes_sent = defaultdict(int)
            bytes_recv = defaultdict(int)
            protocol_counts = defaultdict(Counter)
            # não limpar ip_mac_map para manter mapeamento conhecido

# --------------------
# Signal handler para saída limpa
def handle_sigint(sig, frame):
    global running
    print("\nRecebido SIGINT — finalizando...")
    running = False
    sys.exit(0)

# --------------------
# Main: iniciar sniff + thread de relatório
def main():
    global INTERVAL
    parser = argparse.ArgumentParser(description="Monitor de tráfego por dispositivo (Scapy).")
    parser.add_argument("-i", "--interface", help="Interface para capturar (ex: eth0, wlan0). Se omitido, Scapy escolhe.", default=None)
    parser.add_argument("-t", "--interval", help="Intervalo de relatório em segundos.", type=int, default=INTERVAL)
    args = parser.parse_args()

    INTERVAL = args.interval

    signal.signal(signal.SIGINT, handle_sigint)

    print("Inicializando monitor de tráfego (Scapy).")
    if args.interface:
        print(f"Interface: {args.interface}")
    else:
        print("Interface: (padrão do Scapy)")

    # Thread que imprime relatório periodicamente
    rpt_thread = threading.Thread(target=print_report, args=(INTERVAL,), daemon=True)
    rpt_thread.start()

    # iniciar sniff (captura em tempo real)
    try:
        sniff(iface=args.interface, prn=process_packet, store=False)
    except PermissionError:
        print("Permissão negada: execute o script com privilégios (sudo ou Administrador).")
    except Exception as e:
        print("Erro no sniff:", e)

if __name__ == "__main__":
    main()
