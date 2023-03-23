# asn_nmap

Library created with the aim of facilitating the obtaining of ips service status by asn

Description. 
- The package asn_nmap is used to:
	
	- Asn:
		- get_ips
	- Nmap: 
		- main 

## Requirements

- python3.9 or higher
- nmap

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install asn_nmap

```bash
apt-get install nmap -y
pip install asn-nmap
```

## Usage 

#### Get information from a asn
```python
from asn_nmap.asn import Asn
from asn_nmap.export import Export
from asn_nmap.nmap import Nmap

list_asns = [1251]
ports = [80,443]

asn = Asn()
data = asn.get_ips_by_asns(list_asns)
data = {'1251' : ['200.136.0.0/32']} # Subscribing the data manually to test

nmap = Nmap()
nmap.run_nmap(asn_info=data, port_list=ports, threads_count=1)

Export().to_xlsx(destination_file_name='teste')
```

#### an file will be automatically generated

## Documentation
Project documented with [mkdocs](https://www.mkdocs.org/)

```bash
# Run the command in the root of the project
mkdocs serve
```

## Author
Edgar Reis

## License
[MIT](https://choosealicense.com/licenses/mit/)
