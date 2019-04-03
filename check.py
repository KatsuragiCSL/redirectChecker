#!/usr/bin/python3

import requests, sys, socket
from multiprocessing.dummy import Pool as ThreadPool

def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0

check = sys.argv[1]
domains = sys.argv[2]
pool = ThreadPool(20)
check_list = {}
check = "http://" + check
check = "http://www.starbucks.com"

def checkRedirectDomain(domain):
        if hostname_resolves(domain.strip()):
            try:
                r = requests.get("http://" + domain.strip(), timeout = 3.05, allow_redirects = False)
                if ("Location" in r.headers):
                    check_list[domain.strip()] = r.headers['Location']
            except:
                pass

with open(domains) as f:
    domain_list = f.readlines()
    pool.map(checkRedirectDomain, domain_list)
    pool.close()
    pool.join()
    for x in check_list:
        if check_list[x] != check:
            print(x + "\t" + "Target:" + check_list[x])
