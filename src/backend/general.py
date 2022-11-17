from backend.Flipper_Back import ShowChain


def check_dns_json(file_name):
    try:
        file=open(file_name, 'r')
        print("DNS.json exists")
    except IOError:
        file=open(file_name, 'w+')
        print("DNS.json doesn't exist")

def read_iptables_chain(chain):
    response = ShowChain(chain)
    print(type(response))
    print(response)