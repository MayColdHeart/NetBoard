# NetBoard

Network dashboard v 1.0

O NetBoard é um dashboard de rede voltado para a análise da comunicação entre um determinado servidor e dispositivos conectados à ele. Basicamente o Netboard conta com um sistema de gráficos onde é possível analizar tráfego, protocolos, taxas de upload/download, segurança, alarme e entre outras ferramentas.

##### Linguagens utilizadas
- Python
- ..

## Setup
### Backend
#### User Secrets
Mude o valor de 'Password'.
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=NetboardDB;Username=postgres;Password=postgres"
  }
}
```
