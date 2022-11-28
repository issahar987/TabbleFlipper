from backend import Flipper_Back
import json
import os
from pathlib import Path


def check_dns_json(file_name):
    try:
        file=open(file_name, 'r')
        print("DNS.json exists")
    except IOError:
        file=open(file_name, 'w+')
        print("DNS.json doesn't exist")

def read_iptables():
    print("READ IPTABLES")
    IP_tables = Flipper_Back.ShowRules().split("\n")
    IP_tables_filtered = []
    IP_list = []
    for item in IP_tables:  # delete chain names in IP_tables
        if '-A' in item:
            if item:
                IP_tables_filtered.append(item.split())
    if IP_tables_filtered:
        for item in IP_tables_filtered:
            del item[0]  # delete -A
            del item[1]  # delete -d
            del item[-2:]  # delete -j and DROP
            item[1] = item[1][:-3]  # delete netmask /32
            IP_list.append(item)
    print(IP_list)
    print("END OF READ IPTABLES")
    return IP_list


def get_chain_ips(chain):
    IP_list = read_iptables()
    chain_list = []
    print("READ IPS IN CHAIN")


    for ip in IP_list:
        if ip[0] == chain:  # * Get chain
            chain_list.append(ip)
    print(chain_list)

    print("END OF IPS IN CHAIN")

    return chain_list


def ip_to_dns(chain):
    chain_list = get_chain_ips(chain)

    dns_and_ip_list = []
    path = Path("src/frontend").parent.parent.absolute()
    filename = f'{path}/{chain}_dns.json'

    check_dns_json(filename)
    if os.stat(filename).st_size != 0:
        with open (filename, 'r') as f:
            data = json.load(f)

        for item in chain_list:
            if item[1] in data:
                if data[item[1]] not in dns_and_ip_list:
                    dns_and_ip_list.append(data[item[1]])
            else:
                dns_and_ip_list.append(item[1])

    print(f'dns_list: {dns_and_ip_list}')

    return dns_and_ip_list
