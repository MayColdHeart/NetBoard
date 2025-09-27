import socket
import psutil
import time
import subprocess
import platform
import nmap

#IP
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

#Upload/Download (mbps)
def get_bandwidth(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()
    up_mbps = (net2.bytes_sent - net1.bytes_sent) * 8 / (interval * 1_000_000)
    down_mbps = (net2.bytes_recv - net1.bytes_recv) * 8 / (interval * 1_000_000)
    return up_mbps, down_mbps

#Latência
def ping_host(host="192.168.0.0", count=4): #google or self ip
    param = "-n" if platform.system().lower()=="windows" else "-c"
    command = ["ping", param, str(count), host]
    result = subprocess.run(command, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    for line in lines:
        if "avg" in line or "Average" in line:
            numbers = [s for s in line.replace("=", " ").replace("/", " ").split() if s.replace('.', '').isdigit()]
            if numbers:
                return float(numbers[1])  #média
    return None

# Devices (nmap)
def scan_network(subnet="192.168.0.0/24"):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=subnet, arguments='-sn')
    return scanner.all_hosts()




if __name__ == "__main__":
    print("Netboard v1.0 (early)")
    local_ip = get_local_ip()
    print(f"IP Local: {local_ip}")

    up, down = get_bandwidth()
    print(f"Taxa Upload: {up:.2f} Mbps | Download: {down:.2f} Mbps")

    lat = ping_host()
    if lat:
        print(f"Latência média para 8.8.8.8: {lat} ms")
    else:
        print("Sem medida de latência.")

    print("\nDispositivos ativos")
    devices = scan_network("192.168.0.0/24")
    for d in devices:
        print(" -", d)
