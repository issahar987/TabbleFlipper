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
    
def addJson(IpDns, Chain):
    if (re.match('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', IpDns)):
        return 0
    txtfile = Chain+'_dns.json'
    data = {}
    try:
        with open(txtfile) as f:
            data = json.load(f)
            f.close
    except:
        pass
    with open(txtfile, 'w') as f:
        for item in soc.gethostbyname_ex(IpDns)[2]:
            data[item] = IpDns
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
    print(flagi)  # ['INPUT', '-p --dport 80', 'www.gooogle.com', 'DROP']
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
        print(ip)
        flagi[6]=ip
        print(flagi)
        sb.run(flagi,
            input=os.environ['sudopswd'], encoding="ascii")
    addJson(IpDns, Chain)


def deleteRule(Chain, ChainLinkNumber):
    sb.run(["sudo", "-S", "iptables", "-D", Chain, ChainLinkNumber],
           input=os.environ['sudopswd'], encoding="ascii")
    pass


def exportChain(Chain):
    IP_tables = ShowChain(Chain, "-S")
    # delete first three IPtables string
    IP_tables = IP_tables.splitlines()
    del IP_tables[0]
    print(IP_tables)
    data = {}
    with open(f'{Chain}_export.json', 'w') as file:
        for chainlink in IP_tables:
            chainlink = chainlink.split(" ")
            del chainlink[:1]
            print(chainlink)
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


def importChain(FileName):
    with open(FileName,) as file:
        lines = file.readlines()
        for item in lines:
            item = "sudo -S iptables " + item
            item = item.split(" ")
            del item[-1]
            sb.run(item,
                   input=os.environ['sudopswd'], encoding="ascii")
    pass


def chain_names():
    allrules = ShowRules().split("\n")
    chains = []

    for item in allrules:
        if '-A' not in item:
            if item:
                chains.append(item.split()[1])
    print(chains)

    return chains
