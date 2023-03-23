import pandas as pd
from rich import print as rprint


class Export:

    def __init__(self):
        self.file_output_temp = 'output_temp.txt'

    def to_xlsx(
        self,
        destination_file_name: str = 'asn_nmap_output'
    ) -> None:
        """
        Exportar para arquivo XLSX.

        Parameters:
            destination_file_name: Nome do arquivo de saída.

        Returns:
            Exporta para arquivo XLSX na pasta raiz do projeto.

        Examples:
            >>> from asn_nmap.export import Export
            >>> Export().to_xlsx(destination_file_name='teste')

        """

        try:
            all = pd.read_csv(self.file_output_temp, sep=',', header=None)
            all.columns = ["ASN", "IP", "Port", "Protocol", "State", "Service"]

            port_open_temp = all.loc[all['State'] == 'open']

            port_open = port_open_temp[
                ['ASN', 'IP', 'Port', 'Protocol', 'State', 'Service']
            ]

            dashboard = port_open.groupby(['ASN', 'Port']).size(
            ).reset_index(name='Quantidade')

            with pd.ExcelWriter(f'{destination_file_name}.xlsx') as writer:
                dashboard.to_excel(writer, sheet_name='Dashboard', index=False)
                port_open.to_excel(writer, sheet_name='Port_Open', index=False)
                all.to_excel(writer, sheet_name='All_Info', index=False)

        except FileNotFoundError:
            self.error = True
            rprint(
                "[red]ERRO: Temporary file was not created in the folder[/red]"
            )
