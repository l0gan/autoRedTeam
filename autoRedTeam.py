#! /usr/bin/python

#AutoRedTeam GO!

from ipGen import ipGen
from shareParser import shareParser
from serviceFinder import serviceFinder
import time


if __name__ == "__main__":
    print("[!] Ensure that you are not connected to the network at this time...")
    #raw_input("Press Enter to continue running script...")
    ipGen = ipGen()
    ipsubnet = ipGen.main()
    shareParser = shareParser()
    shareParser.main(ipsubnet)
    time.sleep(30)
    serviceFinder = serviceFinder()
    serviceFinder.main(ipsubnet)
