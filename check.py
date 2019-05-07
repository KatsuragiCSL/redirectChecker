#!/usr/bin/python3

import requests, sys, socket, argparse
from multiprocessing.dummy import Pool
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', help='domain you want to exclude', dest='check', required=True)
parser.add_argument('-w', help='wordlist of domains', dest='domains', required=True)
parse.add_argument('-t', help='number of threads', dest='thread')

args = parser.parse_args()
check = args.check[0]
domains = args.domains[0]
thread = args.thread[0]

check_list = {}
pool = Pool(thread)

def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0

def checkRedirectDomain(domain):
        if hostname_resolves(domain.strip()):
            try:
                r = requests.get("http://" + domain.strip(), timeout = 3.05)
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
        if (parse.path != '/' or parse.netloc != check) :
            print(x + "\t" + "Target:" + check_list[x])
