# 🌐 NetBoard
Sistema de monitoramento de tráfego em servidores HTTP e FTP, onde é realizado a captura de pacotes a partir da interface de rede da máquina local.



## ✨ Funcionalidades
- **Aplicação python**: 
  - Captura de pacotes e envio a API em janelas de 5 segundo.
- **API ASP.NET**: 
  - Processamento e persistência do tráfego em banco de dados.
  - Comunicação em tempo real para servir dashboard.
- **Dashboard**:
  - Visualização do tráfego em tempo real com gráficos de pizza e tempo.
  - Tabela de tráfego com IP de client e tamanhos totais de download/upload.
  - Drill-down por client, com quebra de tráfego por protocolo (FTP, FTP-DATA e HTTP).


## Mídia
*(placehold para imagems)*


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
    cd Netboard
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
    Em um novo terminal, partir da pasta raíz do reposítório.
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
    ```
6. **Acesse as aplicações**
   - Dashboard: http://localhost:5173/
   - API ASP.NET: http://localhost:5043/scalar/
   - Servidores monitorados
     - HTTP: http://localhost:8000/docs
     - FTP: localhost:21


## ⚙ Tecnologias
- **C#**
  - ASP.NET Web API 9
  - SignalR
- **Postgresql**
- **Docker**
- **Javascript**
  - React
  - Chart.js
  - Signal Client
- **Python**
  - Scapy: captação de pacotes
  - Fast API: api
  - pyftpdlib: servidor FTP