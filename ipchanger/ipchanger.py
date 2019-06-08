import configparser
from definitions import ROOT_DIR
from tor.tor import Tor
from utils.ip_analyzer import IPAnalyzer
from utils.logger import Logger
from time import sleep


def main():

    # set up logger instance
    logger = Logger()
    logger.info("start application ipchanger")

    # set up configurations
    config = configparser.ConfigParser()
    config.read(ROOT_DIR + '/cfg/config.ini')

    socks_port = config.getint('tor', 'socks_port')
    control_port = config.getint('tor', 'control_port')
    http_proxy = config.get('tor', 'http_proxy')
    https_proxy = config.get('tor', 'https_proxy')

    analyzer = IPAnalyzer()
    tor = Tor(socks_port=socks_port, control_port=control_port, http_proxy=http_proxy, https_proxy=https_proxy)
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
