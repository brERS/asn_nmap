import requests
from rich import print as rprint


class Asn:

    def __init__(self, asn):
        self.asn = asn
        self.url = f'https://rdap.registro.br/autnum/{self.asn}'
        self.r = requests.get(self.url)
        self.error = False

        if self.r.status_code == 200:
            self.response = self.r.json()
        else:
            self.error = True

    def get_ips(self):
        """ Get ips from asn """

        if self.error is False:
            ips = []
            for x in self.response['links']:
                if x['href'] != self.url:
                    ips.append(x['href'].split('ip/')[-1])
            return ips
        else:
            rprint("[red]Error getting information from asn[/red]")
