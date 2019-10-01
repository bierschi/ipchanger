import configparser
from pyhidentity import ROOT_DIR

from pyhidentity import Logger
from pyhidentity import IPAnalyzer
from pyhidentity import Tor

# set up configuration attributes
config = configparser.ConfigParser()
config.read(ROOT_DIR + '/cfg/config.ini')

socks_port   = config.getint('tor', 'socks_port')
control_port = config.getint('tor', 'control_port')
http_proxy   = config.get('tor', 'http_proxy')
https_proxy  = config.get('tor', 'https_proxy')


def tor_simple():

    analyzer = IPAnalyzer()
    tor = Tor(socks_port=socks_port, control_port=control_port, http_proxy=http_proxy, https_proxy=https_proxy).launch()

    for i in range(3):
        curr_ip = tor.get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("current_ip: %s from country: %s" % (curr_ip, analyzer.get_country_name()))
        tor.request(url="http://www.bierschi.de")
        tor.renew_ip()

    print(tor.get_used_ips())
    tor.kill_process()


def main():

    # set up logger instance
    logger = Logger(name='pyhidentity', level='info', log_folder='/var/log/', debug=True)
    logger.info("start application pyhidentity")

    tor_simple()


if __name__ == '__main__':
    main()
