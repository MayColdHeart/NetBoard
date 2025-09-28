import socket
import psutil
import time
import nmap

# IP local
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Upload/Download (mbps)
def get_bandwidth_mbps(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()
    up_mbps = (net2.bytes_sent - net1.bytes_sent) * 8 / (interval * 1_000_000)
    down_mbps = (net2.bytes_recv - net1.bytes_recv) * 8 / (interval * 1_000_000)
    return up_mbps, down_mbps

# Upload/Download (kbps)
def get_bandwidth_kbps(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()
    up_kbps = (net2.bytes_sent - net1.bytes_sent) * 8 / (interval * 1_000)
    down_kbps = (net2.bytes_recv - net1.bytes_recv) * 8 / (interval * 1_000)
    return up_kbps, down_kbps

# active devices and open doors.
def scan_network(subnet="192.168.0.90", ports="20-1024"):
    """
    subnet: ex: "192.168.0.0/24"
    ports:  ex: "20-1024" ou "80,443,22"

    """
    scanner = nmap.PortScanner()
# active hosts
    scanner.scan(hosts=subnet, arguments='-sn')
    hosts = scanner.all_hosts()

    result = {}
    for host in hosts:
        try:
# find active TCP's doors  
            scanner.scan(hosts=host, arguments=f'-p {ports} -sS')
            result[host] = {}
            for proto in scanner[host].all_protocols():
                result[host][proto] = []
                for port in scanner[host][proto]:
                    state = scanner[host][proto][port]['state']
                    result[host][proto].append((port, state))
        except Exception as e:
            result[host] = {"error": str(e)}
    return result


if __name__ == "__main__":
    print("Netboard v1.0")

    local_ip = get_local_ip()
    print(f"IP Local: {local_ip}")

    up, down = get_bandwidth_mbps()
    print(f"Taxa Upload (mb): {up:.2f} mbps | Download: {down:.2f} mbps")

    up, down = get_bandwidth_kbps()
    print(f"Taxa Upload (Kb): {up:.1f} kbps | Download: {down:.1f} kbps")

    print("Dispositivos e portas/protocolos:")
    devices = scan_network("192.168.0.0/24", ports="20-1024")
    for host, info in devices.items():
        print(f"\nHost: {host}")
        if "error" in info:
            print(f"  Erro: {info['error']}")
            continue
        for proto, ports in info.items():
            print(f"  Protocolo: {proto}")
            for port, state in ports:
                print(f"    Porta {port}/ {proto} -> {state}")