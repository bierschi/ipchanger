import configparser
import logging
from definitions import ROOT_DIR
from tor.tor import Tor
from utils.ip_analyzer import IPAnalyzer
from time import sleep


verbose = False
"""
if verbose:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    logging.info("Verbose output.")
else:
    logging.basicConfig(format="%(levelname)s: %(message)s")

"""


def main():

    config = configparser.ConfigParser()
    config.read(ROOT_DIR + '/cfg/config.ini')

    socks_port = config.getint('tor', 'socks_port')
    control_port = config.getint('tor', 'control_port')

    analyzer = IPAnalyzer()
    tor = Tor(socks_port=socks_port, control_port=control_port)
    p1 = tor.launch()
    i = 0
    j = 0

    while i < 3:
        curr_ip = p1.get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("curr_ip : %s , analyze country: %s" % (curr_ip, analyzer.get_country_name()))
        p1.renew_ip()
        sleep(2)
        i += 1

    print(p1.get_used_ips())
    p1.restart(exit_nodes='{ru}, {us}')

    while j < 3:
        curr_ip = p1.get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("curr_ip : %s , analyze country: %s" % (curr_ip, analyzer.get_country_name()))
        p1.renew_ip()
        sleep(2)
        j += 1

    print(p1.get_used_ips())
    p1.kill_process()


if __name__ == '__main__':
    main()
