import logging
from base_request import BaseRequest


class ProxyRequest(BaseRequest):
    """class ProxyRequest to set up a tor process

    USAGE:
            ProxyRequest()
    """
    def __init__(self, http_proxy=None, https_proxy=None):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class ProxyRequest')

        # init base class
        BaseRequest.__init__(self)

        self.__used_ips = list()

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
        return self.__used_ips

    def save_used_ips(self, ip_address):
        """

        :param ip_address:
        :return:
        """
        if ip_address not in self.__used_ips:
            self.__used_ips.append(ip_address)

