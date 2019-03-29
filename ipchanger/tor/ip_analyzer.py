import requests
import json


class IPAnalyzer:
    """class IPAnalyzer to analyze given ip address

    USAGE:
            IPAnalyzer(ip_address='185.202.19.22')
    """
    def __init__(self, ip_address):
        """

        :param ip_address: string, ip_address
        """

        if isinstance(ip_address, str):
            self.ip_address = ip_address
        else:
            raise TypeError("ip_address must be type of string")

        self.ipdata_service = "https://api.ipdata.co/"

        self.api_key = "?api-key=test"

        # create valid url
        self.url = self.ipdata_service + self.ip_address + self.api_key

        # make a get request and obtain the json object
        self.ipdata_str = json.loads(requests.get(url=self.url).text)

    def get_ipdata(self):
        """get complete ipdata string as a json object

        :return: dict, ipdata json object
        """
        return self.ipdata_str

    def get_city(self):
        """get city

        :return: string, city
        """
        return self.ipdata_str['city']

    def get_region(self):
        """get region

        :return: string, region
        """
        return self.ipdata_str['region']

    def get_country_name(self):
        """get country name

        :return: string, country name
        """
        return self.ipdata_str['country_name']

    def get_country_code(self):
        """get country code

        :return: string, country code
        """
        return self.ipdata_str['country_code']

    def get_continent_name(self):
        """get continent name

        :return: string, continent name
        """
        return self.ipdata_str['continent_name']

    def is_tor(self):
        """is tor ip address

        :return: True, if it is a tor ip address
                 False, if it is not a tor ip address
        """
        return self.ipdata_str['threat']['is_tor']

    def is_proxy(self):
        """is it a proxy

        :return: True, if is a proxy
                 False, if not a proxy
        """
        return self.ipdata_str['threat']['is_proxy']


if __name__ == '__main__':
    ipa = IPAnalyzer(ip_address="87.175.176.44")
    print(ipa.get_country_name())
