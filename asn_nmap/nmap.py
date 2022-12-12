import os
import subprocess

import pandas as pd
from rich import print as rprint


class Nmap:
    """ Class to run nmap scans """

    def __init__(self, asn, ips, ports):
        self.asn = asn
        self.ips = ips
        self.ports = ports
        self.output = None
        self.write = None
        self.file_output_temp = 'output_temp.csv'
        self.error = False

    def main(self):
        """ Main function """

        self.scan_ips()
        if self.error is False:
            self.read_file_to_export()
        if self.error is False:
            self.rm_file()
        if self.error is False:
            rprint("[green]Completed Successfully[/green]")

    def scan_ips(self):
        """ Run nmap scan range"""

        for range in self.ips:

            rprint(f"[blue]INFO: Processing range {range}[/blue]")

            self.output = subprocess.run([
                "nmap",
                "-n",
                "-Pn",
                f"-p{','.join([str(port) for port in self.ports])}",
                f"{range}"
            ], capture_output=True)

            for output_line in self.output.stdout.decode("utf-8").splitlines():  # noqa: E501

                if output_line.count('Nmap scan report for') > 0:
                    ip = output_line.split()[4]

                if output_line.count('tcp') > 0:
                    self.write = f"{self.asn},{ip},{output_line.split()[0].split('/')[0]},{output_line.split()[0].split('/')[1]},{output_line.split()[1]},{output_line.split()[2]}\n"  # noqa: E501
                    self.write_file()

                if output_line.count('udp') > 0:
                    self.write = f"{self.asn},{ip},{output_line.split()[0].split('/')[0]},{output_line.split()[0].split('/')[1]},{output_line.split()[1]},{output_line.split()[2]}\n"  # noqa: E501
                    self.write_file()

    def write_file(self):
        """ Write file """

        try:
            with open(self.file_output_temp, "a") as file:
                file.write(self.write)
        except FileNotFoundError:
            with open(self.file_output_temp, "w") as file:
                file.write(self.write)

    def read_file_to_export(self):
        """Read file to export."""

        try:
            all = pd.read_csv(self.file_output_temp, sep=',', header=None)
            all.columns = ["ASN", "IP", "Port", "Protocol", "State", "Service"]

            port_open_temp = all.loc[all['State'] == 'open']
            port_open = port_open_temp[
                ['ASN', 'IP', 'Port', 'Protocol', 'State', 'Service']
            ]

            dashboard = port_open.groupby(['ASN', 'Port']).size(
            ).reset_index(name='Quantidade')

            with pd.ExcelWriter(f'{self.asn}_output.xlsx') as writer:
                dashboard.to_excel(writer, sheet_name='Dashboard', index=False)
                port_open.to_excel(writer, sheet_name='Port_Open', index=False)
                all.to_excel(writer, sheet_name='All', index=False)
        except FileNotFoundError:
            self.error = True
            rprint(
                "[red]ERRO: Temporary file was not created in the folder[/red]"
            )

    def rm_file(self):
        """ Remove file """

        os.remove(self.file_output_temp)
