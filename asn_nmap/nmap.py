import os
import subprocess
import threading
from time import sleep

from rich import print as rprint


class Nmap:
    """ Class to run nmap scans """

    def __init__(self):
        self.threads = []
        self.write = []
        self.file_output_temp = 'output_temp.txt'
        self._rm_file()

    def run_nmap(
        self,
        asn_info: dict[str, list[str]],
        port_list: list[int],
        threads_count: int = 10
    ) -> list:
        """
        Obtem as informações do status das portas por IP.

        Parameters:
            asn_info: Dicionário com informações de ASN e IPs.
            port_list: Lista de portas a serem verificadas.
            threads_count: Quantidade de threads simultaneamente.

        Returns:
            Lista com informações de status das portas por IP.

        Examples:
            >>> from asn_nmap.nmap import Nmap
            >>> nmap = Nmap()
            >>> data = {
            ...     '1251' : ['200.136.0.0/32']
            ... }
            >>> ports = [80,443]
            >>> nmap.run_nmap(asn_info=data, port_list=ports)
            or
            >>> nmap.run_nmap(asn_info=data, port_list=ports, threads_count=1)
            [
                '1251,200.136.0.0,80,tcp,filtered,http',
                '1251,200.136.0.0,443,tcp,filtered,https'
            ]

        """

        for asn, ips_list in asn_info.items():

            for range in ips_list:

                rprint(
                    f"[blue]INFO: Processing ASN {asn} range {range}[/blue]")

                thread = threading.Thread(
                    target=self._run_thread,
                    name=f'{asn}_{range}',
                    args=(asn, range, port_list)
                )
                self.threads.append(thread)
                thread.start()

                while threading.active_count() > threads_count:
                    sleep(1)

        for thread in self.threads:
            thread.join()

        return self._read_file()

    def _run_thread(self, asn, range, port_list):
        """ Run thread """

        output = subprocess.run([
            "sudo",
            "nmap",
            "-n",
            "-sU",
            "-sS",
            "-Pn",
            f"-p{','.join([str(port) for port in port_list])}",
            f"{range}"
        ], capture_output=True)

        self._format_output(asn, output.stdout.decode("utf-8"))

    def _format_output(self, asn, output):

        for line in output.splitlines():

            if 'Nmap scan report for' in line:
                ip = line.split()[4]

            if 'tcp' in line or 'udp' in line:
                split_line = line.split()
                port = split_line[0].split('/')[0]
                protocol = split_line[0].split('/')[1]
                status = split_line[1]
                service = split_line[2]
                self._write_file(
                    f"{asn},{ip},{port},{protocol},{status},{service}")

    def _write_file(self, write):
        """ Write file """

        try:
            with open(self.file_output_temp, "a") as file:
                file.write(f'{write}\n')
        except FileNotFoundError:
            with open(self.file_output_temp, "w") as file:
                file.write(f'{write}\n')

    def _read_file(self):
        """ Read file """
        try:
            with open(self.file_output_temp, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError as error:
            return [error]

    def _rm_file(self):
        """ Remove file """
        try:
            os.remove(self.file_output_temp)
        except FileNotFoundError:
            pass
