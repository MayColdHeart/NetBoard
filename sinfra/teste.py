import socket
import psutil
import time
from scapy.all import ARP, Ether, srp


def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_bandwidth(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()
    up_mbps = (net2.bytes_sent - net1.bytes_sent) * 8 / (interval * 1_000_000)
    down_mbps = (net2.bytes_recv - net1.bytes_recv) * 8 / (interval * 1_000_000)
    up_kbps = up_mbps * 1000 / 8
    down_kbps = down_mbps * 1000 / 8
    return up_mbps, down_mbps, up_kbps, down_kbps


def scan_network(local_ip):

    base = ".".join(local_ip.split(".")[:3]) + ".0/24"
    print(f"Varredura ARP em {base} ...")

    arp_req = ARP(pdst=base)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_req


    answered = srp(packet, timeout=2, verbose=0)[0]

    print("\nDispositivos ativos:")
    for _, received in answered:
        print(f"IP: {received.psrc:15}  MAC: {received.hwsrc}")


if __name__ == "__main__":
    print("Netboard (Scapy Edition)")

    local_ip = get_local_ip()
    print(f"IP Local: {local_ip}\n")

    scan_network(local_ip)

    print("\n")
    try:
        while True:
            up_mbps, down_mbps, up_kbps, down_kbps = get_bandwidth()
            print(
                f"Upload: {up_mbps:.2f} Mbps ({up_kbps:.1f} Kbps) | "
                f"Download: {down_mbps:.2f} Mbps ({down_kbps:.1f} Kbps)",
                end="\r",
                flush=True,
            )
            scan_network(local_ip)
    except KeyboardInterrupt:
        print("\nEncerrado.")
