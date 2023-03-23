#![logo do projeto](assets/img/logo.png){.logo} ASN NMAP {.title}

Biblioteca criada com o objetivo de facilitar a obtenção do status do serviço ips pelo asn

___
#### Descrição:
O pacote asn_nmap contém as seguintes módulos:

- Asn:
    - get_ips_by_asns
- Nmap: 
    - run_nmap 
- Export:
    - to_xlsx
___
#### Requisitos:

- python3.9 ou superior
- nmap
___
#### Instalação:

Use o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar asn_nmap

```bash
apt-get install nmap -y
pip install asn-nmap
```
___
#### Exemplo de uso:
```python	
# Módulo responsável por obter os ips de um asn
from asn_nmap.asn import Asn

# Módulo responsável por exportar os dados para um arquivo xlsx
from asn_nmap.export import Export 

# Módulo responsável por executar o nmap
from asn_nmap.nmap import Nmap

# Lista de asns
list_asns = [1251]

# Lista de portas
ports = [80, 443]

# Instância do módulo Asn
asn = Asn()

# Obtendo os ips dos asns
data = asn.get_ips_by_asns(list_asns)
data = {'1251' : ['200.136.0.0/32']}  # Reescrevendo o valor de data para o exemplo de uso executar mais rápido.

# Instância do módulo Nmap
nmap = Nmap()

# Executando o nmap
nmap.run_nmap(asn_info=data, port_list=ports, threads_count=50)

# Exportando os dados para um arquivo xlsx
Export().to_xlsx(destination_file_name='teste')
```