from abc import ABC, abstractmethod
import requests


class ProxyRequest(ABC):
    """Abstract Base class ProxyRequest for requests with specific proxies

    """
    def __init__(self):

        self.tor_default_proxies = {
            'http' : 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }

        self.proxies = {
            'http': '',
            'https': ''
        }

        self.session = requests.session()

    def __del__(self):
        """destructor

        """
        pass

    @abstractmethod
    def request(self, url):
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

