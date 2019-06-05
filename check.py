#!/usr/bin/python3

import requests, sys, socket, argparse
from multiprocessing.dummy import Pool
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', help='domain you want to exclude', dest='check', required=True)
parser.add_argument('-w', help='wordlist of domains', dest='domains', required=True)
parser.add_argument('-t', help='number of threads', dest='thread')
parser.add_argument('-x', help='text to be excluded in response', dest='exclude')

args = parser.parse_args()
check = args.check
domains = args.domains
exclude = args.exclude
if args.thread is not None:
    thread = int(args.thread)
else:
    thread = 20

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
                if exclude is not None:
                    if exclude in r.text:
                        pass
                check_list[domain.strip()] = r.url
            except:
                pass

with open(domains) as f:
    domain_list = f.readlines()
    rinse = [urlparse(x).netloc for x in domain_list if '://' in x] + [x for x in domain_list if '://' not in x]
    rinse = list(set(rinse))
    pool.map(checkRedirectDomain, rinse)
    pool.close()
    pool.join()
    for x in check_list:
        parse = urlparse(check_list[x])
        if (parse.path != '/' or parse.netloc != check) :
            print(x + "\t" + "Target:" + check_list[x])
