from pyhidentity import Logger
from pyhidentity import IPAnalyzer
from pyhidentity import Tor

import requests

# set up configuration attributes
socks_port   = 9050
control_port = 9051


def get_current_ip():
    """get current ip address with a request to icanhazip service

    :return: String: current ip address
    """

    session = requests.session()
    session.proxies.update({
        'http': 'socks5://localhost:9050',
        'https': 'socks5://localhost:9050',
    })
    #session.proxies.update({
    #    'http': 'http://localhost:8118',
    #    'https': 'https://localhost:8118',
    #})
    return session.get(url='http://icanhazip.com/').text.rstrip()


def tor_simple():

    analyzer = IPAnalyzer()
    tor = Tor(socks_port=socks_port, control_port=control_port).launch()

    for i in range(5):
        curr_ip = get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("current_ip: %s from country: %s" % (curr_ip, analyzer.get_country_name()))
        tor.trigger_new_ip()

    tor.kill_process()


def tor_with_exit_nodes():

    analyzer = IPAnalyzer()
    tor = Tor(socks_port=socks_port, control_port=control_port).launch(exit_nodes='{ru}, {us}')

    for i in range(3):
        curr_ip = tor.get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("current_ip : %s from country: %s" % (curr_ip, analyzer.get_country_name()))
        tor.renew_ip()

    print(tor.get_used_ips())
    tor.kill_process()


def main():

    # set up logger instance
    logger = Logger(name='pyhidentity', level='info', log_folder='/var/log/', debug=True)
    logger.info("start application pyhidentity")

    tor_simple()
    #tor_with_exit_nodes()


if __name__ == '__main__':
    main()
