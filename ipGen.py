#! /bin/python
import random
import subprocess
import socket, struct, fcntl

def IPDetermine():
        subprocess.call(['./sniffer.sh'])

def Generate():
	f2 = open('IPs.txt', 'r')
	line2 = f2.read()
        randomoctet=random.randint(1,254)
	for line2 in f2:
		lastoctet=line2.split(".")[3]
		if str(randomoctet) == lastoctet:
			print ("regenerating")
			Generate()
	f2.close()
	return str(randomoctet)

def IPGenerate():
        f = open('IP.txt', 'r')
        line=f.read()
        octet1=line.split(".")[0]
        octet2=line.split(".")[1]
        octet3=line.split(".")[2]
        randomoctet=Generate()
        newip=octet1 + '.' + octet2 + '.' + octet3 + '.' + str(randomoctet)
        f.close()
        return(newip)

def ManualIPSet(newip):
	SIOCSIFADDR = 0x8916
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	iface='eth0'
	ip=newip
	bin_ip = socket.inet_aton(ip)
	ifreq = struct.pack('16sH2s4s8s', iface, socket.AF_INET, '\x00'*2, bin_ip, '\x00'*8)
	fcntl.ioctl(sock, SIOCSIFADDR, ifreq)
	print("Your IP has been set to: " + newip)

if __name__ == "__main__":
        IPDetermine()
        newip=IPGenerate()
        ManualIPSet(newip)
