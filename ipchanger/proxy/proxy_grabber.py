import requests
import logging
from bs4 import BeautifulSoup


class ProxyGrabber:
    """class ProxyGrabber to grab different kinds of proxies

    USAGE:
            ProxyGrabber()
    """
    def __init__(self):
        self.logger = logging.getLogger(__file__)

        self.free_proxy_url      = 'https://free-proxy-list.net/'
        self.anonymous_proxy_url = 'https://free-proxy-list.net/anonymous-proxy.html'
        self.us_proxy_url        = 'https://us-proxy.org'
        self.socks_proxy_url     = 'https://socks-proxy.net'
        self.ssl_proxy_url       = 'https://sslproxies.org'

        self.proxy_list = list()

    def get_proxies(self, limit=None):
        """get a list of all proxies, format: ip:port

        :return:list, ip:port as a string
        """

        fp_proxies = self.__get_FreeProxyList_proxies(url=self.free_proxy_url)
        ipadress_proxies = self.__get_IPAdress_proxies()

        self.proxy_list.extend(fp_proxies)
        self.proxy_list.extend(ipadress_proxies)

        if limit is not None:
            return self.proxy_list[:limit]
        else:
            return self.proxy_list

    def get_anonymous_proxies(self):
        """get a list of anonymous proxies

        :return: list, ip:port as a string
        """

        return self.__get_FreeProxyList_proxies(url=self.anonymous_proxy_url)

    def get_us_proxies(self):
        """get a list of us proxies

        :return: list, ip:port as a string
        """
        return self.__get_FreeProxyList_proxies(url=self.us_proxy_url)

    def get_socks_proxies(self):
        """get a list of socks proxies

        :return: list, ip:port as a string
        """
        return self.__get_FreeProxyList_proxies(url=self.socks_proxy_url)

    def get_ssl_proxy(self):
        """get a list of ssl proxies

        :return: list, ip:port as a string
        """
        return self.__get_FreeProxyList_proxies(url=self.ssl_proxy_url)

    def __get_ProxySale_proxies(self):
        """

        :return:
        """
        proxy_sale_url = 'http://free.proxy-sale.com/'
        response = requests.get(url = proxy_sale_url + '?pg-&port[]=http&type[]=an&type[]=el')
        print(response.text)
        soup = BeautifulSoup(response.text, "lxml")
        export_url = soup.find(class_='ico-export-tre').a['href']
        ip_list = requests.get(url = proxy_sale_url + export_url).text.split('\r\n')

        return ip_list[:-1]

    @staticmethod
    def __get_IPAdress_proxies():
        """get proxies from ip-adress.com

        :return: list, ip:port as a string
        """
        response = requests.get(url='https://www.ip-adress.com/proxy-list')
        soup = BeautifulSoup(response.text, 'lxml')
        parser = soup.find('tbody').find_all('tr')
        proxy_list = list()

        for elem in parser:
            elem = elem.get_text().split()[:2]
            if elem[1] != 'transparent':
                proxy_list.append(elem[0])

        return proxy_list

    @staticmethod
    def __get_FreeProxyList_proxies(url):
        """get proxies from FreeProxyList

        :param url: string, url
        :return: list, list of proxies as ip:port
        """
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'lxml')
        proxy_list = list()

        for items in soup.select("tbody tr"):
            proxy = ':'.join([item.text for item in items.select("td")[:2]])
            proxy_list.append(proxy)

        return proxy_list


if __name__ == '__main__':
    grabber = ProxyGrabber()
    proxies = grabber.get_proxies(limit=10)
    print(proxies)
    print(len(proxies))
