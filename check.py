#!/usr/bin/python3

import requests, sys, socket
from multiprocessing.dummy import Pool
from urllib.parse import urlparse

def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0

check = sys.argv[1]
domains = sys.argv[2]
pool = Pool(10)
check_list = {}

def checkRedirectDomain(domain):
        if hostname_resolves(domain.strip()):
            try:
                #r = requests.get("http://" + domain.strip(), timeout = 3.05, allow_redirects = False)
                r = requests.get("http://" + domain.strip(), timeout = 3.05)
                #if ("Location" in r.headers):
                 #   check_list[domain.strip()] = r.headers['Location']
                #else:
                 #   check_list[domain.strip()] = domain.strip()
                check_list[domain.strip()] = r.url
            except:
                pass

with open(domains) as f:
    domain_list = f.readlines()
    pool.map(checkRedirectDomain, domain_list)
    pool.close()
    pool.join()
    for x in check_list:
        parse = urlparse(check_list[x])
        if (o.path != '/' or o.netloc != check):
            print(x + "\t" + "Target:" + check_list[x])
