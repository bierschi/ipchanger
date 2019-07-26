import logging
import requests
from abc import ABC, abstractmethod


class BaseRequest(ABC):
    """Abstract Base class BaseRequest for requests with specific proxies

    """
    def __init__(self):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class BaseRequest')

        self.ip_request_str = "http://icanhazip.com/"
        #self.http_proxy = str(http_proxy)
        #self.https_proxy = str(https_proxy)

        #if ':' not in (self.http_proxy and self.https_proxy):
        #        raise ValueError('')

        # split into ip and port
        #self.http_proxy.split(':')

        self.tor_proxies = {}

        self.proxies = {
            'http': '',
            'https': ''
        }

        self.real_host_ip = requests.get(self.ip_request_str).text
        self.logger.info('real host ip: %s' % self.real_host_ip)

        self.session = requests.session()

        # save used ips in a list
        self.__used_ips = list()

    def get_current_ip(self):
        """get current ip address with a request to icanhazip service

        :return: String: current ip address
        """
        try:

            return self.session.get(url=self.ip_request_str).text.rstrip()

        except ConnectionRefusedError as ex:
            self.logger.error("ConnectionRefusedError: %s" % ex)

    def get_used_ips(self):
        """get list with all ip addresses

        :return: list: containing all used ip addresses
        """
        return self.__used_ips

    def _save_used_ips(self, ip_address):
        """save already used ip addresses in a list

        :param ip_address: string
        """
        if ip_address not in self.__used_ips:
            self.__used_ips.append(ip_address)

    def delete_used_ips(self):
        """

        :return:
        """
        self.__used_ips = list()

    @abstractmethod
    def call(self, url):
        """

        :return:
        """
        pass