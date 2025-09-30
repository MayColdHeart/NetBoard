# Traffic monitor com Scapy.




O script:
- captura pacotes na interface (modo promiscuous)
- agrega bytes por IP e MAC (sent / recv)
- conta protocolos por dispositivo (TCP, UDP, ICMP, ARP)
- tenta mapear protocolos de aplicação por porta (HTTP, HTTPS, DNS, SSH, etc.)
- imprime um relatório no terminal a cada INTERVAL segundos



#### Requisitos de uso do software

- (Instalação do nmap) https://nmap.org/download.html#windows
- (Instalar as dependências do scapy) pip install scapy

