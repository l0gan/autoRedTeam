#! /usr/bin/python

#AutoRedTeam GO!

from ipGen import ipGen
from shareParser import shareParser


if __name__ == "__main__":
    ipGen = ipGen()
    ipsubnet = ipGen.main()
    shareParser = shareParser()
    shareParser.main(ipsubnet)
