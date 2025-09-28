import socket
import psutil
import time
import nmap
import sys


def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_bandwidth_mbps(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()
    up_mbps = (net2.bytes_sent - net1.bytes_sent) * 8 / (interval * 1_000_000)
    down_mbps = (net2.bytes_recv - net1.bytes_recv) * 8 / (interval * 1_000_000)
    return up_mbps, down_mbps


def get_bandwidth_kbps(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()
    up_kbps = (net2.bytes_sent - net1.bytes_sent) * 8 / (interval * 1_000)
    down_kbps = (net2.bytes_recv - net1.bytes_recv) * 8 / (interval * 1_000)
    return up_kbps, down_kbps


def scan_network(subnet="8.8.8.8", ports="20-1024"):

    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments=f"-p {ports} -sS")

    for host in nm.all_hosts():
        print("\n")
        print(f"Host : {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")
        for proto in nm[host].all_protocols():
    
            print(f"Protocol : {proto}")

            lport = sorted(nm[host][proto].keys())
            for port in lport:
                state = nm[host][proto][port]["state"]
                print(f"Port : {port}\tState : {state}")

if __name__ == "__main__":
    print("Netboard v1.0")
    local_ip = get_local_ip()
    print(f"IP Local: {local_ip}\n")

    scan_network()

    try:
        while True:
            up_m, down_m = get_bandwidth_mbps()
            up_k, down_k = get_bandwidth_kbps()
  
            print(
                f"Upload: {up_m:.2f} Mbps | Download: {down_m:.2f} Mbps  "
                f"({up_k:.1f} Kbps / {down_k:.1f} Kbps)   ",
                end="\r",
                flush=True
            )
    except KeyboardInterrupt:
        print("\nEnd.")
        print("\n")
