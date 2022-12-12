import os
import re
import subprocess

import pandas as pd


class Nmap:
    """ Class to run nmap scans """

    def __init__(self):
        self.asn = None
        self.ports = None
        self.output = None
        self.output_clean = None
        self.write = None
        self.file_output_temp = 'output_temp.csv'
        self.file_output = 'output.xlsx'

    def scan_asn(self, asn, ports):
        """ Run nmap scan asn"""
        self.asn = asn
        self.ports = ports

        self.output = subprocess.run([
            "nmap",
            "--script",
            "targets-asn",
            "--script-args",
            f"targets-asn.asn={self.asn}"
        ], capture_output=True)

        self.clear_output_asn()
        self.run_range()
        self.read_file_to_export()
        self.rm_file()

    def clear_output_asn(self):
        """ Clear output """

        self.output_clean = [
            re.sub((r'_| |\|'), '', x)
            for x in self.output.stdout.decode("utf-8").splitlines()
            if x.count('|') > 0 and x.count('.') > 0
        ]

    def run_range(self):
        """ Run nmap scan range"""

        for range in self.output_clean:

            self.output = subprocess.run([
                "nmap",
                "-n",
                "-Pn",
                f"-p{','.join([str(port) for port in self.ports])}",
                f"{range}"
            ], capture_output=True)

            for output_line in self.output.stdout.decode("utf-8").splitlines():

                if output_line.count('Nmap scan report for') > 0:
                    ip = output_line.split()[4]

                if output_line.count('tcp') > 0:
                    self.write = f"{self.asn},{ip},{output_line.split()[0].split('/')[0]},{output_line.split()[0].split('/')[1]},{output_line.split()[1]},{output_line.split()[2]}\n"
                    self.write_file()

                if output_line.count('udp') > 0:
                    self.write = f"{self.asn},{ip},{output_line.split()[0].split('/')[0]},{output_line.split()[0].split('/')[1]},{output_line.split()[1]},{output_line.split()[2]}\n"
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

        df = pd.read_csv(self.file_output_temp, sep=',', header=None)
        df.columns = ["ASN", "IP", "Port", "Protocol", "State", "Service"]

        def2 = df.loc[df['State'] == 'open']
        df2 = def2[['ASN', 'IP', 'Port', 'Protocol', 'State', 'Service']]

        df3 = df2.groupby(['ASN', 'Port']).size(
        ).reset_index(name='Quantidade')

        with pd.ExcelWriter(self.file_output) as writer:
            df3.to_excel(writer, sheet_name='Dashboard', index=False)
            df2.to_excel(writer, sheet_name='Port Open', index=False)
            df.to_excel(writer, sheet_name='All', index=False)


    def rm_file(self):
        """ Remove file """

        os.remove(self.file_output_temp)
