from scapy.all import sniff, IP, TCP
from collections import defaultdict
import time

INTERVAL = 5  # report interval in seconds

# Map server ports to protocol names
PORT_PROTO = {
    21: "FTP",
    60000: "FTP-DATA", 60001: "FTP-DATA", 60002: "FTP-DATA",
    60003: "FTP-DATA", 60004: "FTP-DATA", 60005: "FTP-DATA",
    60006: "FTP-DATA", 60007: "FTP-DATA", 60008: "FTP-DATA",
    60009: "FTP-DATA", 60010: "FTP-DATA",
    8000: "HTTP",
}

# Data storage: {(ip, protocol): [upload_bytes, download_bytes]}
traffic = defaultdict(lambda: [0, 0])

def map_port_to_proto(port: int):
    # Handle FTP-DATA range 60000–60010
    if 60000 <= port <= 60010:
        return "FTP-DATA"
    return PORT_PROTO.get(port)

def process_packet(pkt):
    if IP not in pkt or TCP not in pkt:
        return
    ip = pkt[IP]
    tcp = pkt[TCP]

    proto = map_port_to_proto(tcp.sport) or map_port_to_proto(tcp.dport)
    if not proto:
        return

    size = len(pkt)

    # Determine upload/download relative to IP
    # If the source IP is the server, it's upload; else download
    traffic[(ip.src, proto)][0] += size  # upload
    traffic[(ip.dst, proto)][1] += size  # download

def human_readable_kbps(bytes_count, interval):
    bits_per_sec = (bytes_count * 8) / interval
    return round(bits_per_sec / 1000)

def report():
    global traffic
    while True:
        time.sleep(INTERVAL)
        if not traffic:
            print("No traffic detected...")
            continue

        report_data = []

        print("\nTraffic report:")
        print(f"{'IP':<15} {'Protocol':<10} {'Up(Kbps)':>10} {'Down(Kbps)':>12} {'Total(Kbps)':>12}")
        print("-" * 600)
        for (ip, proto), (up, down) in traffic.items():
            total = up + down
            up_kbps = human_readable_kbps(up, INTERVAL)
            down_kbps = human_readable_kbps(down, INTERVAL)
            total_kbps = human_readable_kbps(total, INTERVAL)

            print(f"{ip:<15} {proto:<10} {up_kbps:>10} {down_kbps:>12} {total_kbps:>12}")

            # Compatible with CreateTrafficWindowDto
            report_data.append({
                "DeviceIp": ip,
                "ProtocolName": proto,
                "UploadSizeKbps": up_kbps,
                "DownloadSizeKbps": down_kbps,
                "TotalSizeKbps": total_kbps
            })

        # Reset counters for next interval
        traffic.clear()

if __name__ == "__main__":
    import threading
    threading.Thread(target=report, daemon=True).start()
    sniff(prn=process_packet, store=False)