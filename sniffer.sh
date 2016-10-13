#! /bin/sh

tcpdump -s0 -i eth0 -c 100 -nn | awk '{ print gensub(/(.*)\..*/,"\\1","g",$3), $4, gensub(/(.*)\..*/,"\\1","g",$5) }' | grep -E '^(192\.168|10\.|172\.1[6789]\.|172\.2[0-9]\.|172\.3[01]\.)'| awk '{print $1}'| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'> IPs.txt

cat IPs.txt |uniq -c | sort -n | tail -n1 | awk '{print $2}'> IP.txt
