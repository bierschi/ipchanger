import requests
import logging
from bs4 import BeautifulSoup


class ProxyGrabber:
    """class ProxyGrabber to grab different kinds of proxies

    USAGE:
            grabber = ProxyGrabber()
            grabber.get_proxies()
    """
    def __init__(self):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info("create class ProxyGrabber")

        self.free_proxy_url      = 'https://free-proxy-list.net/'
        self.anonymous_proxy_url = 'https://free-proxy-list.net/anonymous-proxy.html'
        self.us_proxy_url        = 'https://us-proxy.org'
        self.socks_proxy_url     = 'https://socks-proxy.net'
        self.ssl_proxy_url       = 'https://sslproxies.org'

        self.proxy_list = list()

    def get_proxies(self, num=None):
        """get a list of all proxies, format: ip:port

        :param num: number of proxies
        :return:list, ip:port as a string
        """

        fp_proxies = self.__parse_free_proxy_page(url=self.free_proxy_url)
        ipadress_proxies = self.__parse_ipadress_page()

        self.proxy_list.extend(fp_proxies)
        self.proxy_list.extend(ipadress_proxies)

        if num is not None:
            self.logger.info("get %d proxies" % len(self.proxy_list[:num]))
            # TODO check limit attribute
            return self.proxy_list[:num]
        else:
            self.logger.info("get %d proxies" % len(self.proxy_list))
            return self.proxy_list

    def get_anonymous_proxies(self):
        """get a list of anonymous proxies

        :return: list, ip:port as a string
        """

        return self.__parse_free_proxy_page(url=self.anonymous_proxy_url)

    def get_us_proxies(self):
        """get a list of us proxies

        :return: list, ip:port as a string
        """
        return self.__parse_free_proxy_page(url=self.us_proxy_url)

    def get_socks_proxies(self):
        """get a list of socks proxies

        :return: list, ip:port as a string
        """
        return self.__parse_free_proxy_page(url=self.socks_proxy_url)

    def get_ssl_proxies(self):
        """get a list of ssl proxies

        :return: list, ip:port as a string
        """
        return self.__parse_free_proxy_page(url=self.ssl_proxy_url)

### parser ####

    def parse_proxysale_page(self):
        """ parses proxies from free.proxy-sale.com

        :return: list, ip:port as a string
        """
        proxy_sale_url = 'http://free.proxy-sale.com/'
        response = requests.get(url=proxy_sale_url + '?pg-&port[]=http&type[]=an&type[]=el')
        soup = BeautifulSoup(response.text, "html.parser")
        export_url = soup.find(class_='ico-export-tre').a['href']
        ip_list = requests.get(url=proxy_sale_url + export_url).text.split('\r\n')

        return ip_list[:-1]

    def __parse_ipadress_page(self):
        """parses proxies from ip-adress.com

        :return: list, ip:port as a string
        """
        response = requests.get(url='https://www.ip-adress.com/proxy-list')
        soup = BeautifulSoup(response.text, "html.parser")
        parser = soup.find('tbody').find_all('tr')
        proxy_list = list()

        for elem in parser:
            elem = elem.get_text().split()[:2]
            if elem[1] != 'transparent':
                if ('-' in elem[0]) or (not elem[0]) or (':' not in elem[0]) or ('.' not in elem[0]):
                    pass
                else:
                    proxy_list.append(elem[0])

        return proxy_list

    def __parse_free_proxy_page(self, url):
        """parses given url from free-proxy-list.net

        :param url: string, url
        :return: list, list of proxies as ip:port
        """
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, "html.parser")
        proxy_list = list()

        for items in soup.select("tbody tr"):
            proxy = ':'.join([item.text for item in items.select("td")[:2]])
            if ('-' in proxy) or (not proxy) or (':' not in proxy) or ('.' not in proxy):
                pass
            else:
                proxy_list.append(proxy)

        return proxy_list


if __name__ == '__main__':
    grabber = ProxyGrabber()
    print(grabber.get_proxies())
    #proxies = grabber.get_proxies(limit=10)
    #print(proxies)
    #print(len(proxies))
