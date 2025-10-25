# 🌐 NetBoard
Sistema de monitoramento de tráfego em servidores HTTP e FTP, onde é realizado a captura de pacotes a partir da interface de rede da máquina local. <br>
O objetivo do projeto é analisar o tráfego de rede em uma subnet, então é preciso de no mínimo dois dispositivos para verificar o funcionamento.


## ✨ Funcionalidades
- **Aplicação python**: 
- **API ASP.NET**: 
  - Processamento e persistência do tráfego em banco de dados.
  - Comunicação em tempo real para servir dashboard.
- **Dashboard**:
  - Visualização do tráfego em tempo real com gráficos de pizza e tempo.
  - Tabela de tráfego com IP de client e tamanhos totais de download/upload.
  - Drill-down por client, com quebra de tráfego por protocolo (FTP, FTP-DATA e HTTP).


## Mídia
<details>
  <summary><b>Dashboard</b></summary>
  <img width="1347" height="597" alt="Dashboard" src="https://github.com/user-attachments/assets/7599d71b-1b6f-4ec1-bf3b-42e3e7c818ff" />
</details>

<details>
  <summary><b>Arquitetura</b></summary>
  <img width="881" height="814" alt="Arquitetura" src="https://github.com/user-attachments/assets/b720663f-0f9b-4798-9e0c-0a16e79242c3" />
</details>

<details>
  <summary><b>API ASP.NET</b></summary>
  <img width="277" height="265" alt="API ASP.NET" src="https://github.com/user-attachments/assets/19586adc-f8a7-4770-9c14-a972e5e0be58" />
  <img width="795" height="736" alt="SignalR Hub" src="https://github.com/user-attachments/assets/ffae5394-b9de-4e45-95e0-a19c64794477" />
</details>

<details>
  <summary><b>Banco de Dados</b></summary>
  <img width="828" height="746" alt="Banco de Dados" src="https://github.com/user-attachments/assets/158dfd9c-3928-4553-bd4b-ba3fc62eabda" />
</details>

<details>
  <summary><b>Servidor HTTP (FastAPI)</b></summary>
  <img width="1555" height="465" alt="HPTT FastAPI" src="https://github.com/user-attachments/assets/bda47e6d-fde9-4d2d-bd94-cee04284774f" />
</details>

<details>
  <summary><b>Servidor FTP (pyftpdlib)</b></summary>
  <img width="464" height="353" alt="FTP SERVER" src="https://github.com/user-attachments/assets/16fcc2ab-8009-4929-9000-85355fa2c773" />
</details>

## 🛠 Instalação
### Pré-requisitos
- [Docker](https://www.docker.com/get-started/)
- [Node.js](https://nodejs.org/en/download)
- [.NET 9 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/9.0)
- [Python 3](https://www.python.org/downloads/)

### Etapas
1. **Clone o repositório**
    ```bash
    git clone https://github.com/MayColdHeart/NetBoard.git
    cd NetBoard
    ```

2. **Configure variáveis de ambiente**
    ```
    cp .example.env .env
    ```
   Caso precise, edite a senha do usuário postgres no banco de dados, dentro do arquivo `.env`.

3. **Execute servidores (HTTP e FTP) e API com docker**
    ```bash
    docker compose up
    ```
    Aguarde todos os containers executarem.

4. **Execute o sniffer de pacotes** <br>
    Em um novo terminal, a partir da pasta raíz do reposítório.
    ```bash
    cd sinfra
    python -m venv venv
    ```
    Ative o ambiente virtual:
    - Linux bash
      ```bash
      source .env/bin/activate
      ```
    - Windows cmd
      ```bash
      .env\Scripts\activate.bat
      ```
    Instale os requerimentos:
    ```bash
    pip install -r requirements.txt
    ```
    Execute:
    ```bash
    python sinfra.py
    ```

5. **Execute o dashboard** <br>
    Em um novo terminal
    ```bash
    cd design
    npm i
    npm run dev
    ```

6. **Acesse as aplicações**
   - Teste o funcionamento de cada servidor localmente, para verificar se tudo está funcionando corretamente.
   - Dashboard: http://localhost:5173/
   - API ASP.NET: http://localhost:5043/scalar/
   - Servidores monitorados
     - ⚠ O acesso aos servidores de maneira local não serão registrados no dashboard, apenas o tráfego externo de rede.
     - HTTP: http://localhost:8000/docs
     - FTP:
       - Hostname: localhost
       - Porta: 21
       - Usuário: guest
       - Senha: (vazio)

7. **Configurando firewall**
  - É preciso criar regras no firewall para permitir conexão entre máquinas em rede local, sem que seja exposto o acesso a internet pública.
  - Para isso, verifique o IP da sua máquina na rede local e a máscara de rede para saber o range de IPs que serão permitidos o acesso.
  - 🔎 Verifique o IP e a máscara de rede
    - Linux (bash)
      ```bash
      ifconfig
      ```
    - Windows (PowerShell ou cmd)
      ```powershell
      ipconfig
      ```
    - No caso do linux, use alguma calculadora de sub-rede para traduzir para notação CIDR:
      - Exemplo: IP `192.168.1.5` com máscara `255.255.255.0` → sub-rede `192.168.1.0/24`
      - Exemplo: IP `172.30.56.27` com máscara `255.255.240.0` → sub-rede `172.30.48.0/20`
    - Anote o IP da sua máquina (ex: `192.168.1.5`), que será o servidor, e da sub-rede (ex: `192.168.1.0/24`)
  - Criando regras de firewall
    - A seguir, serão abertas portas **apenas para a rede local**
    - Substitua `192.168.0.0/24` pela faixa da sua rede local
    - Linux (bash - usando UFW)
      ```bash
      # Caso inativo, ative o UFW
      ufw enable

      # FTP (porta 21 + faixa 60000–60010)
      sudo ufw allow from 192.168.0.0/24 to any port 21 proto tcp
      sudo ufw allow from 192.168.0.0/24 to any port 60000:60010 proto tcp

      # HTTP (porta 8000)
      sudo ufw allow from 192.168.0.0/24 to any port 8000 proto tcp

      # Verificar regras
      sudo ufw status numbered
      ```

    - Windows (PowerShell - usando Windows Defender Firewall)
      ```powershell
      # FTP: porta 21 + range 60000–60010
      New-NetFirewallRule -DisplayName "FTP Local Server (Local Subnet)" `
        -Direction Inbound -Protocol TCP `
        -LocalPort 21,60000-60010 `
        -RemoteAddress LocalSubnet -Action Allow

      # HTTP: porta 8000
      New-NetFirewallRule -DisplayName "HTTP Local Server (Local Subnet)" `
        -Direction Inbound -Protocol TCP -LocalPort 8000 `
        -RemoteAddress LocalSubnet -Action Allow

      # Verificar regras
      Get-NetFirewallPortFilter |
          Where-Object { $_.LocalPort -match '^(21|60000-60010|8000)$' } |
          Get-NetFirewallRule |
          Select-Object DisplayName, Direction, Enabled
      ```

8. **Acessando servidores em outra máquina** <br>
Conecte outra máquina na mesma rede, que será usada como client. <br>
Lembre de utilizar o IP da sua máquina servidor, que foi anotado no passo 7. <br>
Então, substitua `<ip-servidor-local>` pelo seu IP.
  - HTTP:
    - Acesse com seu browser 
    - `http://<ip-servidor-local>:8000/docs`
  - FTP:
    - Utilize algum cliente FTP com suporte a modo passivo e comando `EPSV`, como o `ftp` do bash (Linux) ou WinSCP (Windows)
      - ⚠ **Exemplos sem suporte**: `ftp` dos terminais Windows não tem suporte ao modo passivo e `FileZilla` no linux não utiliza `EPSV`, mas sim `PASV` para estabelecer conexão, causando falha
    - Hostname: `<ip-servidor-local>`
    - Porta: 21
    - Usuário: guest
    - Senha: (vazio)

9. **Visualize o tráfego de rede**
- Acesse os endpoints do servidor HTTP com seu client e/ou movimente arquivos entre do client para o servidor com FTP.
- Na sua máquina servidor, acesse o dashboard: http://localhost:5173/.
- Visualize o tráfego.

10. **Removendo regras do firewall (opcional)**
  - **Use caso não esteja mais utilizando o projeto**. Assim removendo regras desnecessárias do firewall.
  - Linux (bash - usando UFW)
    ```bash
    # Remover regra pelo número da lista
    sudo ufw status numbered
    sudo ufw delete <número_da_regra>
    ```
  - Windows (PowerShell)
    ```powershell
    # Remover regra pelo DisplayName
    Remove-NetFirewallRule -DisplayName "FTP Local Server (Local Subnet)"
    Remove-NetFirewallRule -DisplayName "HTTP Local Server (Local Subnet)"
    ```


## ⚙ Tecnologias
- **C#**
  - ASP.NET Web API 9
  - SignalR
  - Entity Framework 
- **Postgresql**
- **Docker**
- **Javascript**
  - React
  - Chart.js
  - Signal Client
- **Python**
  - Scapy
  - Fast API
  - pyftpdlib
