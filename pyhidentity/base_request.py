import logging
import requests
from abc import ABC, abstractmethod


class BaseRequest(ABC):
    """Abstract Base class BaseRequest for requests with specific proxies

    """
    def __init__(self, http_proxy, https_proxy=None):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class BaseRequest')

        self.http_proxy = str(http_proxy)
        self.https_proxy = str(https_proxy)

        if ':' not in (self.http_proxy and self.https_proxy):
                raise ValueError('')

        # split into ip and port
        #self.http_proxy.split(':')

        self.proxies = {
            'http': self.http_proxy,
            'https': self.https_proxy
        }

        self.session = requests.session()

    @abstractmethod
    def call(self, url):
        """

        :return:
        """
        pass

    @abstractmethod
    def get_current_ip(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def get_used_ips(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def save_used_ips(self, ip_address):
        """

        :param ip_address:
        :return:
        """
        pass
