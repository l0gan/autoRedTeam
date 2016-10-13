#! /bin/python
import random
import subprocess
import socket, struct, fcntl
import string
import os
import sys

class ipGen():
    def IPDetermine(self):
            subprocess.call(['./sniffer.sh'])

    def Generate(self):
        f2 = open('IPs.txt', 'r')
        line2 = f2.read()
        randomoctet=random.randint(1,254)
        for line2 in f2:
            lastoctet=line2.split(".")[3]
            if str(randomoctet) == lastoctet:
                print ("regenerating")
                self.Generate()
        f2.close()
        return str(randomoctet)

    def macchanger(self):
            print("Changing MAC Address...")
            os.system("ifconfig eth0 down")
            os.system("macchanger -r eth0")
            print("Your MAC address has been changed.")
            os.system("ifconfig eth0 up")

    def id_generator(self, size=4, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def hostnameChanger(self):
        number=self.id_generator()
        randomfile=random.choice(os.listdir("names/"))
        randomname=random.choice(open("names/" + randomfile).readlines())
        hostnameNew=(randomname.rstrip("\n") + "-" + number)
        os.system("cp /etc/hostname /etc/hostname.orig")
        os.system("echo " + hostnameNew + " > /etc/hostname")
        os.system("service hostname.sh")

    def IPGenerate(self):
        f = open('IP.txt', 'r')
        line=f.read()
        octet1=line.split(".")[0]
        octet2=line.split(".")[1]
        octet3=line.split(".")[2]
        ipsubnet=octet1 + "." + octet2 + "." + octet3 + ".0/24"
        randomoctet=self.Generate()
        newip=octet1 + '.' + octet2 + '.' + octet3 + '.' + str(randomoctet)
        f.close()
        return(newip, ipsubnet)

    def ManualIPSet(self, newip):
        SIOCSIFADDR = 0x8916
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        iface='eth0'
        ip=newip
        bin_ip = socket.inet_aton(ip)
        ifreq = struct.pack('16sH2s4s8s', iface, socket.AF_INET, '\x00'*2, bin_ip, '\x00'*8)
        fcntl.ioctl(sock, SIOCSIFADDR, ifreq)
        print("Your IP has been set to: " + newip)

    def main(self):
        self.hostnameChanger()
        self.macchanger()
        self.IPDetermine()
        newip, ipsubnet=self.IPGenerate()
        self.ManualIPSet(newip)
        return ipsubnet
