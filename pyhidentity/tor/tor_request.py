import logging
from base_request import BaseRequest
from tor.tor import Tor


class TorRequest(BaseRequest):
    """ Class TorRequest for generating requests with ip addresses from the tor network

    """
    def __init__(self, socks_port, control_port, http_proxy='127.0.0.1:8118', https_proxy='127.0.0.1:8118'):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class TorRequest')

        self.socks_port = socks_port
        self.control_port = control_port

        # init base class
        BaseRequest.__init__(self)

        # init tor class
        self.tor = Tor(socks_port=socks_port, control_port=control_port, http_proxy=http_proxy, https_proxy=https_proxy).launch()

        if http_proxy:
            self.proxies['http'] = http_proxy
        if https_proxy:
            self.proxies['https'] = https_proxy
        else:
            # default tor proxy
            self.proxies = {
                'http': 'socks5://127.0.0.1:{}'.format(self.socks_port),
                'https': 'socks5://127.0.0.1:{}'.format(self.socks_port)
            }

        # set proxies
        self.session.proxies = self.proxies

        self._save_used_ips(self.get_current_ip())

    def __del__(self):
        """destructor

        """
        self.quit()

    def quit(self):
        """

        :return:
        """
        self.tor.kill_process()

    def call(self, url):
        """

        :return:
        """

        self.logger.info("request url: %s with proxy: %s" % (url, self.proxies['http']))
        self.session.get(url=url)

    def new_identity(self):
        """

        :return:
        """
        new_ip = self.__renew_ip()
        self.logger.info("renewed the ip address to: %s" % new_ip)

        self._save_used_ips(ip_address=new_ip)

    def set_countries(self, countries):
        """

        :param countries:
        :return:
        """
        self.delete_used_ips()
        self.tor = self.tor.restart(exit_nodes=countries)

    def __renew_ip(self):
        """renew current ip address, this can take a while

        :return: string, new ip address
        """

        old_ip = new_ip = self.get_current_ip()

        while old_ip == new_ip:

            old_ip = new_ip
            self.tor.trigger_new_ip()
            new_ip = self.get_current_ip()

        return new_ip
