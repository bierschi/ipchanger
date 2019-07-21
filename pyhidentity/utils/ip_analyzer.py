import requests
import json
import logging


class IPAnalyzer:
    """class IPAnalyzer to analyze given ip address

    USAGE:
           analyzer = IPAnalyzer()
    """
    def __init__(self):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class IPAnalyzer')

        self.ip_address = None
        self.url = None
        self.ipdata_str = None
        self.ip_set = False

        self.ipdata_service = "https://api.ipdata.co/"
        self.api_key = "?api-key=test"

    def set_ip(self, ip_address):
        """sets a ip address

        :param ip_address: string
        """

        if isinstance(ip_address, str):
            self.ip_address = ip_address
            self.logger.info("set ip address to %s" % ip_address)
        else:
            self.logger.error("ip_address must be type of string")
            raise TypeError("ip_address must be type of string")

        # create valid url
        self.url = self.ipdata_service + self.ip_address + self.api_key

        # make a get request and obtain the json object
        self.ipdata_str = json.loads(requests.get(url=self.url).text)
        self.ip_set = True

    def get_ipdata(self):
        """get complete ipdata string as a json object

        :return: dict, ipdata json object
        """
        if self.ip_set:
            return self.ipdata_str

    def get_city(self):
        """get city

        :return: string, city
        """
        if self.ip_set:
            return self.ipdata_str['city']

    def get_region(self):
        """get region

        :return: string, region
        """
        if self.ip_set:
            return self.ipdata_str['region']

    def get_country_name(self):
        """get country name

        :return: string, country name
        """
        if self.ip_set:
            return self.ipdata_str['country_name']

    def get_country_code(self):
        """get country code

        :return: string, country code
        """
        if self.ip_set:
            return self.ipdata_str['country_code']

    def get_continent_name(self):
        """get continent name

        :return: string, continent name
        """
        if self.ip_set:
            return self.ipdata_str['continent_name']

    def is_tor(self):
        """is tor ip address

        :return: True, if it is a tor ip address
                 False, if it is not a tor ip address
        """
        if self.ip_set:
            return self.ipdata_str['threat']['is_tor']

    def is_proxy(self):
        """is it a proxy

        :return: True, if is a proxy
                 False, if not a proxy
        """
        if self.ip_set:
            return self.ipdata_str['threat']['is_proxy']


if __name__ == '__main__':
    ip = IPAnalyzer()
    ip.set_ip(ip_address='46.173.214.3')
    print(ip.get_ipdata())
