import random
import logging
from pyhidentity.proxy.grabber import ProxyGrabber
import requests

class ProxyProvider(ProxyGrabber):
    """class ProxyProvider to provide proxies

    USAGE:
            provider = ProxyProvider()
    """

    proxy_pool = dict()

    def __init__(self):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info("create class ProxyProvider")

        super().__init__(timeout=100, max_workers=8)

        self.session = requests.Session()

        self.set_proxy_pool()

    def __del__(self):
        pass

    def set_proxy_pool(self):
        """

        :return:
        """
        self.proxy_pool = self.collect_proxies()
        print(len(self.proxy_pool['http']))

    def get(self):

        try:
            tmp_proxy = self.proxy()
            print(tmp_proxy)
            proxies = dict()
            proxies['http'] = tmp_proxy
            proxies['https'] = tmp_proxy
            return self.session.get(url="https://google.de", proxies=proxies, timeout=2)
        except Exception as e:
            #print(e)
            return self.get()

    def proxy(self):

        index = random.randint(0, len(self.proxy_pool['http']) -1)

        return self.proxy_pool['http'][index]

    def http_proxies(self, num=None):
        """ get only http proxies

        :return: list, ip:port as a string
        """
        return self.proxy_pool['http'][:num]

    def socks4_proxies(self):
        """ get only socks4 proxies

        :return: list, ip:port as a string
        """
        return self.proxy_pool['socks4']

    def socks5_proxies(self):
        """ get only socks5 proxies

        :return: list, ip:port as a string
        """
        return self.proxy_pool['socks5']


if __name__ == '__main__':
    provider = ProxyProvider()
    #proxies = provider.http_proxies()
    #print(proxies)
    #print(provider.http_proxies(5))
    for i in range(0, 10):
        resp = provider.get()
        print(resp.content)