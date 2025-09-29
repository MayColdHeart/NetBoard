import time
import threading
from collections import defaultdict, Counter
from scapy.all import sniff, Ether, IP, TCP, UDP, ICMP, ARP, Raw
import signal
import sys


INTERVAL = 5
MAX_TABLE_ROWS = 200 

PORT_PROTO = {
    80: "HTTP",
    443: "HTTPS",
    53: "DNS",
    67: "DHCP/BOOTP",
    68: "DHCP/BOOTP",
    22: "SSH",
    21: "FTP",     
    20: "FTP-DATA", 
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

bytes_sent = defaultdict(int)    # up
bytes_recv = defaultdict(int)    # down
protocol_counts = defaultdict(Counter) 
ip_mac_map = {}  
_lock = threading.Lock()

running = True

def key_from_pkt(ip, mac):
    return (ip, mac)

def map_port_to_proto(port):
    return PORT_PROTO.get(port, str(port))

def detect_app_by_payload(payload_bytes):
    if not payload_bytes:
        return None
    
    start = payload_bytes[:16].upper() if len(payload_bytes) >= 16 else payload_bytes.upper()
    http_signs = [b"GET ", b"POST ", b"HEAD ", b"PUT ", b"DELETE ", b"OPTIONS ", b"HTTP/"]
    for s in http_signs:
        if s in start or payload_bytes.upper().find(s) != -1:
            return "HTTP"
    
    ftp_signs = [b"USER ", b"PASS ", b"220 ", b"230 ", b"530 ", b"331 "]
    for s in ftp_signs:
        if s in start or payload_bytes.upper().find(s) != -1:
            return "FTP"
    return None

def process_packet(pkt):
    try:
        with _lock:
            if ARP in pkt:
                arp = pkt[ARP]
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
                size = len(pkt) 

                if src_mac and src_ip:
                    ip_mac_map[src_ip] = src_mac
                if dst_mac and dst_ip:
                    ip_mac_map[dst_ip] = dst_mac

                key_src = key_from_pkt(src_ip, ip_mac_map.get(src_ip, src_mac))
                key_dst = key_from_pkt(dst_ip, ip_mac_map.get(dst_ip, dst_mac))

                bytes_sent[key_src] += size
                bytes_recv[key_dst] += size

                if TCP in pkt:
                    tcp = pkt[TCP]
                    sport = tcp.sport
                    dport = tcp.dport
                    protocol_counts[key_src].update(["TCP"])
                    protocol_counts[key_dst].update(["TCP"])
                    protocol_counts[key_src].update([map_port_to_proto(dport)])
                    protocol_counts[key_dst].update([map_port_to_proto(sport)])

                    payload = b""
                    if Raw in pkt:
                        try:
                            payload = bytes(pkt[Raw].load)
                        except Exception:
                            payload = b""
      
                    app_by_payload = detect_app_by_payload(payload)
                    if app_by_payload == "HTTP":
                        protocol_counts[key_src].update(["HTTP"])
                    elif app_by_payload == "FTP":
                        protocol_counts[key_src].update(["FTP"])

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
                    protocol_counts[key_src].update([f"IP/{ip.proto}"])
                    protocol_counts[key_dst].update([f"IP/{ip.proto}"])
            else:
                size = len(pkt)
                key = key_from_pkt("unknown", src_mac)
                bytes_sent[key] += size
                protocol_counts[key].update(["NON-IP"])
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
    global bytes_sent, bytes_recv, protocol_counts, ip_mac_map
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

            if not sorted_keys:
                print("no response..")
            else:
                print(f"{'IP':<18} {'Up':>12} {'Down':>12} {'Total':>12}  Protocols (top)")
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
                    top_protocols = ", ".join([f"{p}({c})" for p, c in prot_counter.most_common(5)])
                    print(f"{ip:<18} {mac:<20} {up_str:>12} {down_str:>12} {total_str:>12}  {top_protocols}")
            print("="*100)

            bytes_sent = defaultdict(int)
            bytes_recv = defaultdict(int)
            protocol_counts = defaultdict(Counter)

def handle_sigint(sig, frame):
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
