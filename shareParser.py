#! /bin/python

import subprocess
import os
import re
from socket import *
import nmap

# Share Parser will look through a share and attempt to find sensitive data. Data includes:
#	   - Passwords (looks for files named Password.txt or similar)
#	   - SSNs
#	   - Credit Card Numbers
#	   - More?
root = 'mnt'

def nmapPortScan():
	port='111'
	hosts='172.16.133.134'
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

# Connect to NFS share
def nfsmount(ip):
	results=subprocess.check_output('showmount -e ' + ip, shell=True)
	results=results.split('\n')
	anonNFS=results[1]
	if '*' in anonNFS or 'anonymous' in anonNFS:
		print('[!] Anonymous NFS share found!')
		results=anonNFS.split(' ')[0]
		results=str(results)
		print('[+] Mounting NFS share: ' + results)
		subprocess.check_output('mount -t nfs '+ ip + ':' + results + ' ' + root, shell=True)
		print('[+] NFS share mounted to ' + root)
		subprocess.check_output('cd ' + root, shell=True)
		fileSearch(root)
		# unmount share
		print('[+] Unmounting mount: ' + results)
		subprocess.check_output('umount ' + root, shell=True)
	else:
		print('[-] No Anonymous NFS shares found')


def fileSearch(root):
	print('[+] Searching for files in: ' + root)
	for path, subdirs, files in os.walk(root):
		for name in files:
			ssnSearch(path, name)
			CCSearch(path, name)
		#passSearch(files, path)
		for subdir in subdirs:
			fileSearch(subdir)

def passSearch(files, path):
	print('[+] Looking for password files')
	for file in files:
		if 'password' in file.lower():
			print('[!] Potential Password File: ' + path + file)

def CCSearch(path, name):
	print('[+] Looking for Credit Card Numbers in: ' + path + '/' + name)
	with open(path + '/' + name, 'r') as f:
		for line, number in enumerate(f, 1):
			prog = re.compile('(\D|^)\%?[Bb]\d{13,19}\^[\-\/\.\w\s]{2,26}\^[0-9][0-9][01][0-9][0-9]{3}|(\D|^)\;\d{13,19}\=(\d{3}|)(\d{4}|\=)|[1-9][0-9]{2}\-[0-9]{2}\-[0-9]{4}\^\d|(\D|^)5[1-5][0-9]{2}(\ |\-|)[0-9]{4}(\ |\-|)[0-9]{4}(\ |\-|)[0-9]{4}(\D|$)|(\D|^)4[0-9]{3}(\ |\-|)[0-9]{4}(\ |\-|)[0-9]{4}(\ |\-|)[0-9]{4}(\D|$)|(\D|^)(34|37)[0-9]{2}(\ |\-|)[0-9]{6}(\ |\-|)[0-9]{5}(\D|$)|(\D|^)30[0-5][0-9](\ |\-|)[0-9]{6}(\ |\-|)[0-9]{4}(\D|$)|(\D|^)(36|38)[0-9]{2}(\ |\-|)[0-9]{6}(\ |\-|)[0-9]{4}(\D|$)|(\D|^)6011(\ |\-|)[0-9]{4}(\ |\-|)[0-9]{4}(\ |\-|)[0-9]{4}(\D|$)')
			result = prog.search(number)
			if result:
				print('[!] MATCH: Credit Card Data found in line number: ' + str(line))
		f.close()

def ssnSearch(path, name):
	print('[+] Looking for SSNs in: ' + path + '/' + name)
	with open(path + '/' + name, 'r') as f:
		for line, number in enumerate(f, 1):
			# Look for SSNs with - and with spaces
			prog = re.compile('(\D|^)[0-9]{3}\-[0-9]{2}\-[0-9]{4}(\D|$)|(\D|^)[0-9]{3}\ [0-9]{2}\ [0-9]{4}(\D|$)')
			result = prog.search(number)
			if result:
				print('[!] MATCH: SSN Data found in line number: ' + str(line))
		f.close()

if __name__ == '__main__':
	IP = nmapPortScan()
	for ip in IP:
		try:
			nfsmount(ip)
		except:
			print('[-] An error occurred. Skipping host: ' + ip)
			pass
