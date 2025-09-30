
import time
import threading
from collections import defaultdict, Counter
from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
import signal
import sys
from typing import Optional
import requests

BACKEND_URL = "http://localhost:5000/api/monitor"

INTERVAL = 5
MAX_TABLE_ROWS = 200 
PORT_PROTO = {
    8000: "HTTP",
    21: "FTP",     
    20: "FTP-DATA", 
    443: "HTTPS",
    53: "DNS",
    25: "SMTP",
}



bytes_sent = defaultdict(int)
bytes_recv = defaultdict(int)
protocol_counts = defaultdict(Counter)
_lock = threading.Lock()
running = True

def map_port_to_proto(port: int) -> Optional[str]: #(6000–6010)
    if 6000 <= port <= 6010:
        return "FTP-DATA"
    return PORT_PROTO.get(port)

def detect_app_by_payload(payload_bytes):
    if not payload_bytes:
        return None
    
    start = payload_bytes[:16].upper() if len(payload_bytes) >= 16 else payload_bytes.upper()
    http_signs = [b"GET ", b"POST ", b"HEAD ", b"PUT ", b"DELETE ", b"OPTIONS ", b"HTTP/"]
    for s in http_signs:
        if s in start or payload_bytes.upper().find(s) != -1:
            return "HTTP"
    
    ftp_signs = [b"USER ", b"PASS ", b"220 ", b"230 ", b"530 ", b"331 "] #Reply code
    for s in ftp_signs:
        if s in start or payload_bytes.upper().find(s) != -1:
            return "FTP"
    return None

def process_packet(pkt):
    try:
        with _lock:
            if IP not in pkt:
                return  

            ip = pkt[IP]
            src_ip = ip.src
            dst_ip = ip.dst
            size = len(pkt)
            bytes_sent[src_ip] += size
            bytes_recv[dst_ip] += size


            if TCP in pkt:
                tcp = pkt[TCP]
                sport, dport = tcp.sport, tcp.dport

  
                if sport in PORT_PROTO or dport in PORT_PROTO:
                    protocol_counts[src_ip].update(["TCP"])
                    protocol_counts[dst_ip].update(["TCP"])

                    if dport in PORT_PROTO:
                        protocol_counts[src_ip].update([map_port_to_proto(dport)])
                    if sport in PORT_PROTO:
                        protocol_counts[dst_ip].update([map_port_to_proto(sport)])

      
                    if Raw in pkt:
                        try:
                            payload = bytes(pkt[Raw].load)
                        except Exception:
                            payload = b""
                        else:
                            app = detect_app_by_payload(payload)
                            if app:
                                protocol_counts[src_ip].update([app])


            elif UDP in pkt:
                udp = pkt[UDP]
                sport, dport = udp.sport, udp.dport

                if sport in PORT_PROTO or dport in PORT_PROTO:
                    protocol_counts[src_ip].update(["UDP"])
                    protocol_counts[dst_ip].update(["UDP"])
                    if dport in PORT_PROTO:
                        protocol_counts[src_ip].update([map_port_to_proto(dport)])
                    if sport in PORT_PROTO:
                        protocol_counts[dst_ip].update([map_port_to_proto(sport)])

    except Exception:
        return


def human_readable_rate(bytes_count, interval):
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
    global bytes_sent, bytes_recv, protocol_counts
    while running:
        time.sleep(interval)
        with _lock:
            print("\n" + "="*100)
            print(f"{interval}, {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-"*100)
            keys = set(bytes_sent.keys()) | set(bytes_recv.keys()) | set(protocol_counts.keys())
            def total_bytes(k):
                return bytes_sent.get(k, 0) + bytes_recv.get(k, 0)
            sorted_keys = sorted(keys, key=total_bytes, reverse=True)[:MAX_TABLE_ROWS]

            report_data = []

            if not sorted_keys:
                print("no response..")
            else:
                print(f"{'IP':<18} {'Up':>12} {'Down':>12} {'Total':>12}  Protocols (top)")
                print("-"*100)
                for ip in sorted_keys:
                    up_b = bytes_sent.get(ip, 0)
                    down_b = bytes_recv.get(ip, 0)
                    total_b = up_b + down_b
                    up_str = human_readable_rate(up_b, interval)
                    down_str = human_readable_rate(down_b, interval)
                    total_str = human_readable_rate(total_b, interval)
                    prot_counter = protocol_counts.get(ip, Counter())
                    top_protocols = ", ".join([f"{p}({c})" for p, c in prot_counter.most_common(5)])
                    print(f"{ip:<18} {up_str:>12} {down_str:>12} {total_str:>12}  {top_protocols}")
                    # Adiciona ao relatório para envio
                    report_data.append({
                        "ip": ip,
                        "up_Bps": up_b // interval,  # bytes por segundo
                        "down_Bps": down_b // interval,
                        "total_Bps": total_b // interval,
                        "protocols": dict(prot_counter.most_common(5)),
                        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                    })
            print("="*100)

            # Envia os dados para o backend
            if report_data:
                try:
                    response = requests.post(BACKEND_URL, json=report_data, timeout=3)
                    if response.status_code != 200:
                        print(f"[WARN] Falha ao enviar dados para backend: {response.status_code}")
                except Exception as e:
                    print(f"[ERRO] Não foi possível enviar dados ao backend: {e}")

            bytes_sent = defaultdict(int)
            bytes_recv = defaultdict(int)
            protocol_counts = defaultdict(Counter)
def handle_sigint(signum, frame):
    global running
    print("\nfinishing")
    running = False
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handle_sigint)

    print("Starting NetBoard")
    print("Interface: scapy")

    rpt_thread = threading.Thread(target=print_report, args=(INTERVAL,), daemon=True)
    rpt_thread.start()

    try:
        sniff(iface=None, prn=process_packet, store=False)
    except PermissionError:
        print("permission deny!")
    except Exception as e:
        print("Error", e)

if __name__ == "__main__":
    main()
