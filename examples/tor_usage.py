from pyhidentity import Logger
from pyhidentity import IPAnalyzer
from pyhidentity import Tor

# set up configuration attributes
socks_port   = 9050
control_port = 9051
http_proxy   = '127.0.0.1:8118'  # default for privoxy
https_proxy  = '127.0.0.1:8118'  # default for privoxy


def tor_simple():

    analyzer = IPAnalyzer()
    tor = Tor(socks_port=socks_port, control_port=control_port, http_proxy=http_proxy, https_proxy=https_proxy).launch()

    for i in range(3):
        curr_ip = tor.get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("current_ip: %s from country: %s" % (curr_ip, analyzer.get_country_name()))
        tor.renew_ip()

    print(tor.get_used_ips())
    tor.kill_process()


def tor_with_exit_nodes():

    analyzer = IPAnalyzer()
    tor = Tor(socks_port=socks_port, control_port=control_port, http_proxy=http_proxy, https_proxy=https_proxy).launch(exit_nodes='{ru}, {us}')

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
    tor_with_exit_nodes()


if __name__ == '__main__':
    main()
