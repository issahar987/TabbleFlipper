import subprocess as sb
import os
import re
import json
import socket as soc


def EnterSudo(passwd):
    os.environ['sudopswd'] = passwd
    print(sb.run(["sudo", "-S", "cat", "INPUT_dns.json"],
                          input=os.environ['sudopswd'], encoding="ascii"))
    pass

def get_host_dict(IpDns):
    if (re.match('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', IpDns)):
        return 0
    data = {}
    print(IpDns)
    print(soc.gethostbyname_ex(IpDns))
    for item in soc.gethostbyname_ex(IpDns)[2]:
            data[item] = IpDns

    return data
    
def addJson(Ips, Chain):
    file_name = Chain+'_dns.json'
    data = {}
    try:
        with open(file_name) as f:
            data = json.load(f)
            f.close
    except:
        pass
    with open(file_name, 'w') as f:
        for ip in Ips:
            data[ip] = Ips[ip]
        json.dump(data, f, ensure_ascii=False, indent=4)
    pass


def ShowRules():
    response = sb.check_output(["sudo", "-S", "iptables", "-S"],
                               input=os.environ['sudopswd'], encoding="ascii")
    return response


def ShowChain(Chain, flaga=None):
    if flaga == None:
        response = sb.check_output(["sudo", "-S", "iptables", "-L", Chain, "--line-numbers"],
                                   input=os.environ['sudopswd'], encoding="ascii")
        return response
    response = sb.check_output(["sudo", "-S", "iptables", "-S", Chain],
                               input=os.environ['sudopswd'], encoding="ascii")
    return response


def ClearAll():
    sb.run(["sudo", "-S", "iptables", "--flush"],
           input=os.environ['sudopswd'], encoding="ascii")
    pass


def AddRule(flagi):
    print(f'used flags: {flagi}')  # ['INPUT', '-p --dport 80', 'www.gooogle.com', 'DROP']
    Chain=flagi[0]
    IpDns=flagi[2]
    IPs = get_host_dict(IpDns)
    if IPs == 0:
        IPs = [IpDns]
    start = ["sudo", "-S", "iptables", "-A"]
    start.reverse()
    for item in start:
        flagi.insert(0, item)
    flagi.insert(-1, "-j")
    # ['sudo', '-S', 'iptables', '142.250.179.174', 'INPUT', '-d', 'youtube.com', '-j', 'DROP']

    for ip in IPs:
        flagi[6]=ip
        sb.run(flagi,
            input=os.environ['sudopswd'], encoding="ascii")
    addJson(IPs, Chain)


def deleteRule(Chain, ChainLinkNumber):
    sb.run(["sudo", "-S", "iptables", "-D", Chain, ChainLinkNumber],
           input=os.environ['sudopswd'], encoding="ascii")
    pass


def exportChain(Chain):
    IP_tables = ShowChain(Chain, "-S")
    # delete first three IPtables string
    IP_tables = IP_tables.splitlines()
    del IP_tables[0]
    data = {}
    with open(f'{Chain}_export.json', 'w') as file:
        for chainlink in IP_tables:
            chainlink = chainlink.split(" ")
            del chainlink[:1]
            ip = chainlink[2][:-3]  # delete netmask /32
            print(type(chainlink[2][:-3]))
            print(soc.gethostbyaddr(ip))
            print(type(soc.gethostbyaddr(ip)))
            data[soc.gethostbyaddr(ip)[0]] = {
                    #"iplist": soc.gethostbyname((soc.gethostbyaddr(chainlink[3]))[0]),
                    "direction": chainlink[1],
                    "action": chainlink[4],
                    "chainname": chainlink[0],
                    }
        json.dump(data, file, ensure_ascii=False, indent=4)
    pass


def importChain(Chain):
    data = {}

    with open(f'{Chain}_export.json', 'r') as file:
        data = json.load(file)
        flagi = [] # ['INPUT', '-p --dport 80', 'www.gooogle.com', 'DROP']
        for item in data:
            print(data[item])
            flagi.append(data[item]['chainname'])
            flagi.append(data[item]['direction'])
            flagi.append(item)
            flagi.append(data[item]['action'])
            AddRule(flagi)


def chain_names():
    allrules = ShowRules().split("\n")
    chains = []

    for item in allrules:
        if '-A' not in item:
            if item:
                chains.append(item.split()[1])

    return chains
