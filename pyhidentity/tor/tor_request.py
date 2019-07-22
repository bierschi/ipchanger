import logging
from base_request import BaseRequest
from tor.tor import Tor


class TorRequest(BaseRequest):
    """Abstract Base class ProxyRequest for requests with specific proxies

    """
    def __init__(self, socks_port, control_port, http_proxy=None, https_proxy=None):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class TorRequest')

        self.socks_port = socks_port
        self.control_port = control_port

        # init base class
        BaseRequest.__init__(self, http_proxy=http_proxy, https_proxy=https_proxy)

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

    def __del__(self):
        """destructor

        """
        pass

    def call(self, url):
        """

        :return:
        """

        self.logger.info("request url: %s with proxy: %s" % (url, self.proxies['http']))
        self.session.proxies = self.proxies
        self.session.get(url=url)

    def get_current_ip(self):
        """

        :return:
        """
        pass

    def get_used_ips(self):
        """

        :return:
        """
        pass

    def save_used_ips(self, ip_address):
        """

        :param ip_address:
        :return:
        """
        pass