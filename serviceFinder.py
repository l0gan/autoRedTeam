#! /bin/python
import random
import subprocess
import socket, struct, fcntl
import string
import os
import sys
import nmap
import time

class serviceFinder():
    def dnsFind(self, ipsubnet):
        port='53'
        hosts=ipsubnet
        IP = []
        print('[+] Scanning ' + hosts + ' for port ' + port)
        nm=nmap.PortScanner()
        scan_results=nm.scan(hosts, port)
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                lport.sort()
                for port in lport:
                    if nm[host][proto][port]['state'] == 'open':
                        IP.append(host)
        return(IP)

    def adFind(self, ipsubnet):
        port='389'
        hosts=ipsubnet
        IP = []
        print('[+] Scanning ' + hosts + ' for port ' + port)
        nm=nmap.PortScanner()
        scan_results=nm.scan(hosts, port)
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                lport.sort()
                for port in lport:
                    if nm[host][proto][port]['state'] == 'open':
                        IP.append(host)
        return(IP)

    def ADenum(self, ADIPs):
        for IP in ADIPs:
            os.system('enum4linux ' + IP + ' > ' + IP + '.enum')

    def DNSZT(self, DNSIPs):
        for IP in ADIPs:
            os.system('dig @' + IP + ' axfr > ' + IP + '.dnszt')

    def main(self, ipsubnet):
        DNSIPs = self.dnsFind(ipsubnet)
        self.DNSZT(DNSIPs)
        # Wait 5 min to check for AD servers
        time.sleep(300)
        ADIPs = self.adFind(ipsubnet)
        self.ADenum(ADIPs)
