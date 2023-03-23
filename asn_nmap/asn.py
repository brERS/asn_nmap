import requests


class Asn:

    def __init__(self):
        self.asns = []
        self.response = {}

    def get_ips_by_asns(self, asns: list[int]) -> dict[str, list[str]]:
        """
        Recebe uma lista de ASNs a serem consultados.

        parameters:
            asns: ASNs a serem consultados.

        returns:
            Um dicionario com os ASNs e seus respectivos ips.

        Examples:
            >>> from asn_nmap.asn import Asn
            >>> asn = Asn()
            >>> list_asns = [1251]
            >>> asn.get_ips_by_asns(list_asns)
            {'1251': ['200.136.0.0/16', '200.18.240.0/20', ...]}
        """

        self.asns = asns

        for asn in asns:
            self.response[asn] = self._get_ips(asn)

        return self.response

    def _get_ips(self, asn):
        ips = []

        url = f'https://rdap.registro.br/autnum/{asn}'

        response_get = requests.get(url)

        if response_get.status_code == 200:

            for resp in response_get.json()['links']:

                if resp['href'] != url:
                    ips.append(resp['href'].split('ip/')[-1])

            return ips
        else:
            return ['Erro ao obter ips do ASN']
