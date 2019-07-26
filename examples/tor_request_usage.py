from pyhidentity import Logger
from pyhidentity import IPAnalyzer
from pyhidentity import TorRequest

# set up configuration attributes
socks_port   = 9050
control_port = 9051
http_proxy   = '127.0.0.1:8118'  # default for privoxy
https_proxy  = '127.0.0.1:8118'  # default for privoxy


def main():
    # set up logger instance
    logger = Logger(name='pyhidentity', level='info', log_folder='/var/log/', debug=True)
    logger.info("start application pyhidentity")

    analyzer = IPAnalyzer()
    tor_req = TorRequest(socks_port=socks_port, control_port=control_port, http_proxy=http_proxy, https_proxy=https_proxy)
    #tor_req = TorRequest(socks_port=socks_port, control_port=control_port)

    for i in range(3):
        curr_ip = tor_req.get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("current_ip: %s from country: %s" % (curr_ip, analyzer.get_country_name()))
        tor_req.new_identity()

    #print(tor_req.get_used_ips())
    tor_req.quit()

    """
    
    tor_req.set_countries('{ru}, {us}')
    for i in range(3):
        curr_ip = tor_req.get_current_ip()
        analyzer.set_ip(ip_address=curr_ip)
        print("current_ip: %s from country: %s" % (curr_ip, analyzer.get_country_name()))
        tor_req.new_identity()
    print(tor_req.get_used_ips())
    """

if __name__ == '__main__':
    main()
