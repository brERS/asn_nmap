# asn_nmap

Library created with the aim of facilitating the obtaining of ips service status by asn

Description. 
- The package asn_nmap is used to:
	
	- Asn:
		- get_ips
	- Nmap: 
		- main 


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
apt-get install nmap -y
pip install asn-nmap
```

## Usage 

#### Get information from a asn
```python
from asn_nmap.asn import Asn
from asn_nmap.nmap import Nmap

asn = '15169'
port_scan = [80, 443]

asn_response = Asn(asn)

Nmap(asn, asn_response.get_ips(), port_scan).main()
```

#### an output.xlsx file will be automatically generated

## Author
Edgar Reis

## License
[MIT](https://choosealicense.com/licenses/mit/)
