import threading
from scapy.all import sniff, IP, TCP
from collections import defaultdict
import socket
import time
import requests

INTERVAL = 5  # report interval in seconds

PORT_PROTO = {
    21: "FTP",
    8000: "HTTP",
}
FTP_DATA_RANGE = range(60000, 60011)

# Data storage: {(external_ip, protocol): [upload_bytes, download_bytes]}
traffic = defaultdict(lambda: [0, 0])
traffic_lock = threading.Lock()  # Lock to avoid race conditions

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

LOCAL_IP = get_local_ip()
print(f"Local IP detected: {LOCAL_IP}")

def map_port_to_proto(port: int):
    if port in PORT_PROTO:
        return PORT_PROTO[port]
    if port in FTP_DATA_RANGE:
        return "FTP-DATA"
    return None

def process_packet(pkt):
    if IP not in pkt or TCP not in pkt:
        return
    ip = pkt[IP]
    tcp = pkt[TCP]

    proto = map_port_to_proto(tcp.sport) or map_port_to_proto(tcp.dport)
    if not proto:
        return

    size = len(pkt)

    # Only count traffic relative to external IPs
    with traffic_lock:
        if ip.src == LOCAL_IP:
            traffic[(ip.dst, proto)][0] += size
        elif ip.dst == LOCAL_IP:
            traffic[(ip.src, proto)][1] += size

def human_readable_kbps(bytes_count, interval):
    bits_per_sec = (bytes_count * 8) / interval
    return bits_per_sec / 1000  # float Kbps

def report():
    while True:
        time.sleep(INTERVAL)
        with traffic_lock:
            items = list(traffic.items())
            traffic.clear()  # Reset safely while locked

        if not items:
            print("No traffic detected...")
            continue

        print("\nTraffic report:")
        print(f"{'External IP':<15} {'Protocol':<10} {'Up(Kbps)':>10} {'Down(Kbps)':>12} {'Total(Kbps)':>12}")
        print("-" * 70)

        for (ip, proto), (up, down) in items:
            total = up + down
            up_kbps = human_readable_kbps(up, INTERVAL)
            down_kbps = human_readable_kbps(down, INTERVAL)
            total_kbps = human_readable_kbps(total, INTERVAL)

            print(f"{ip:<15} {proto:<10} {up_kbps:>10.2f} {down_kbps:>12.2f} {total_kbps:>12.2f}")

            try:
                resp = requests.post(
                    "http://localhost:5043/network/traffic-window",
                    headers={"Content-Type": "application/json"},
                    json={
                        "deviceIp": ip,
                        "protocolName": proto,
                        "uploadSizeKbps": up_kbps,
                        "downloadSizeKbps": down_kbps,
                        "totalSizeKbps": total_kbps
                    }
                )
            except Exception as e:
                print(f"Failed to POST data for {ip} ({proto}): {e}")

if __name__ == "__main__":
    threading.Thread(target=report, daemon=True).start()
    sniff(prn=process_packet, store=False)
