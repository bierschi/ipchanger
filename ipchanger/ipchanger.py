import configparser
from definitions import ROOT_DIR
from tor.tor import Tor
from tor.ip_analyzer import IPAnalyzer


def main():

    config = configparser.ConfigParser()
    config.read(ROOT_DIR + '/cfg/config.ini')

    socks_port = config.getint('tor', 'socks_port')
    control_port = config.getint('tor', 'control_port')

    tor = Tor(socks_port=socks_port, control_port=control_port)
    tor_p1 = tor.launch()

    analyzer = IPAnalyzer()

    current_ip = tor_p1.get_current_ip()
    analyzer.set_ip(current_ip)
    print(analyzer.get_country_name())

    for i in range(0, 3):

        new_ip = tor.renew_ip()
        analyzer.set_ip(new_ip)
        print(analyzer.get_country_name())

    print(tor_p1.get_used_ips())


if __name__ == '__main__':
    main()
