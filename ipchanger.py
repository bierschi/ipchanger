import configparser
from ipchanger.definitions import ROOT_DIR
from ipchanger.tor.tor import Tor


def main():

    config = configparser.ConfigParser()
    config.read(ROOT_DIR + '/cfg/config.ini')

    socks_port = config.getint('tor', 'socks_port')
    control_port = config.getint('tor', 'control_port')

    tor = Tor(socks_port=socks_port, control_port=control_port)
    tor_p1 = tor.launch()

    print(tor_p1.get_current_ip())

    for i in range(0, 3):

        tor.renew_ip()

    print(tor_p1.get_used_ips())


if __name__ == '__main__':
    main()
