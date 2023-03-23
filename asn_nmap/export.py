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

            all_data = pd.read_csv(
                'output_temp.txt', 
                header=None, 
                names=["ASN", "IP", "Port", "Protocol", "State", "Service"]
            )

            # O Nmap divide as portas em seis estados:
            states = dict.fromkeys(
                [
                    'open',
                    'closed',
                    'filtered',
                    'unfiltered',
                    'open|filtered',
                    'closed|filtered'
                ],
                ''
            )


            for state in states:
                states[state] = all_data.loc[all_data['State'] == state]


            dashboard = all_data.groupby(
                ['ASN', 'Port', 'Protocol', 'State']
            ).size().reset_index(name='Quantidade')


            with pd.ExcelWriter(f'{destination_file_name}.xlsx') as writer:
                
                dashboard.to_excel(writer, sheet_name='Dashboard', index=False)

                for state_name, state_data in states.items():
                    if not state_data.empty:
                        state_data.to_excel(
                            writer,
                            sheet_name=f'state_{state_name}',
                            index=False
                        )

                all_data.to_excel(writer, sheet_name='All_Info', index=False)

        except FileNotFoundError:
            rprint(
                "[red]ERRO: Temporary file was not created in the folder[/red]"
            )
