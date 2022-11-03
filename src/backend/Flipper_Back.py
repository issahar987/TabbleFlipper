import subprocess as sb
import os
import re
import json
import socket as soc


def EnterSudo(passwd):
    os.environ['sudopswd'] = passwd
    pass


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
    for item in soc.gethostname(IpDns):
        data[item] = IpDns
    with open(txtfile, 'w') as f:
        json.dump(data, f)
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


def AddRule(Chain, SourcDest, IpDns, WhatDo):
    sb.run(["sudo", "-S", "iptables", "-A", Chain, SourcDest, IpDns, "-j", WhatDo],
           input=os.environ['sudopswd'], encoding="ascii")
    addJson(IpDns, Chain)


def deleteRule(Chain, ChainLinkNumber):
    sb.run("sudo", "-S", "iptables", "-D", Chain, ChainLinkNumber,
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
            del chainlink[:2]
            print(chainlink)
            data[soc.gethostbyaddr(chainlink[2])] = {
                    #"iplist": soc.gethostbyname((soc.gethostbyaddr(chainlink[3]))[0]),
                    "direction": chainlink[1],
                    "action": chainlink[4],
                    "chainname": chainlink[0],
                    }
        json.dump(data, file)
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


EnterSudo("")
