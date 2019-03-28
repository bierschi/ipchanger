import configparser
from ipchanger.definitions import ROOT_DIR
from ipchanger.tor.tor_connection import TorConnection


def main():

    config = configparser.ConfigParser()
    config.read(ROOT_DIR + '/cfg/config.ini')

    password = config.get('tor', 'password')
    address = config.get('tor', 'address')
    port = config.getint('tor', 'port')

    tor = TorConnection(password=password, address=address, port=port)

    print("current ip: %s" % tor.get_current_ip())

    for i in range(0, 2):
        tor.renew_ip()

    print(tor.get_used_ips())


if __name__ == '__main__':
    main()
