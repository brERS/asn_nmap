# asn_nmap

Library created with the aim of facilitating the obtaining of ips service status by asn

Description. 
- The package asn_nmap is used to:
	
	- Nmap: 
		- scan_asn 


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
apt-get install nmap -y
pip install asn-nmap
```

## Usage 

#### Get information from a asn
```python
from asn_nmap.nmap import Nmap

nmap = Nmap()
nmap.scan_asn(15169, [80, 443])
```

#### an output.xlsx file will be automatically generated

## Author
Edgar Reis

## License
[MIT](https://choosealicense.com/licenses/mit/)
