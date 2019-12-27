import logging
import requests
from abc import ABC, abstractmethod


class BaseRequest(ABC):
    """Abstract Base class BaseRequest for requests with specific proxies

    """
    def __init__(self):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class BaseRequest')

        self.icanhazip = "http://icanhazip.com/"
        self.real_host_ip = requests.get(self.icanhazip).text
        self.logger.info('real host ip: %s' % self.real_host_ip)

        # create a request session
        self.session = requests.session()

        self.proxies = {
            'http': '',
            'https': '',
            'socks': ''
        }

        self.tor_proxies = {}

        # save used ips in a list
        self.__used_ips = list()

    def __del__(self):
        """ destructor

        """
        self.session.cookies.clear()
        self.session.close()

    def get_current_ip(self):
        """get current ip address with a request to icanhazip service

        :return: String: current ip address
        """
        try:

            return self.session.get(url=self.icanhazip).text.rstrip()

        except ConnectionRefusedError as ex:
            self.logger.error("ConnectionRefusedError: %s" % ex)

    def get_used_ips(self):
        """get list with all used ip addresses

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
        """ deletes the used ips container

        """
        self.__used_ips = list()

    @abstractmethod
    def new_identity(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def get(self, url, **kwargs):
        """ sends a get request

        :param url: url for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        pass

    @abstractmethod
    def post(self, url, data=None, json=None, **kwargs):
        """ sends a post request

        :param url: url for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        pass

    @abstractmethod
    def put(self, url, data=None, **kwargs):
        """ sends a put request

        :param url: url for the request
        :param data: data for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        pass

    @abstractmethod
    def delete(self, url, **kwargs):
        """ sends a delete request

        :param url: url for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        pass
