import requests
import logging
from multiprocessing import Process, Manager

from ipchanger.proxy.proxy_grabber import ProxyGrabber
from time import sleep

class ProxyChecker:
    """class ProxyChecker to check if the proxy is up or dead

    USAGE:
            ProxyChecker(timeout=1)
    """
    def __init__(self, timeout=1):
        self.logger = logging.getLogger('ipchanger')
        self.logger.info("create class ProxyChecker")

        self.ping_url = "http://www.google.com"

        if isinstance(timeout, (int, float)):
            self.timeout = timeout
        else:
            self.logger.error("timeout must be type of int")
            raise TypeError("timeout must be type of int")

        self.proxy_list = None
        self.proxy_up   = None
        self.proxy_dead = None

        self.processes = None

    def __del__(self):
        pass

    def restart(self, proxies, size=20):

        self.processes = list()
        self.run(proxies=proxies, size=size)

    def run(self, proxies, size=20):
        """starts the proxy check routine

        """

        if isinstance(proxies, list):
            # TODO check format ip:port

            self.proxy_list = proxies
            self.processes = list()
            self.proxy_up = Manager().list()
            self.proxy_dead = Manager().list()
            self.__process_handler(size=size)

            [p.start() for p in self.processes]
            [p.join() for p in self.processes]

        else:
            self.logger.error("'proxies must be type of list, containing proxies in format ['ip:port']")
            raise TypeError("'proxies must be type of list, containing proxies in format ['ip:port']")

    def get_proxies_up(self):
        """returns all proxies which are alive

        :return: list, containing all alive proxies (ip:port)
        """
        return self.proxy_up

    def get_proxies_dead(self):
        """returns all proxies which are dead

        :return: list, containing all dead proxies (ip:port)
        """
        return self.proxy_dead

    def __make_proxy_sublists(self, size=100):
        """divides proxy list in multiple sublists with 'size'

        :return:lists in list, multiple sublists with size 'size'
        """

        return [self.proxy_list[x:x+size] for x in range(0, len(self.proxy_list), size)]

    def __process_handler(self, size=20):
        """depending on the size of sublists, creating multiple processes

        """

        proxy_sub_list = self.__make_proxy_sublists(size=size)
        
        for i in range(len(proxy_sub_list)):
            p = Process(target=self.__check_proxy, args=(proxy_sub_list[i],))
            self.processes.append(p)

    def __check_proxy(self, proxy_list):
        """checks if a proxy responses to a request within a given timeout

        :return: list, list with active proxies
        """

        for i, proxy in enumerate(proxy_list):

            try:

                response = requests.get(url=self.ping_url, proxies={"http": proxy, "https": proxy, "socks": proxy},
                                        timeout=self.timeout)

                if response.status_code == 200:
                    # TODO check list if proxy already in
                    self.proxy_up.append(proxy)
                else:
                    self.proxy_dead.append(proxy)

            except requests.Timeout:
                self.logger.warning("Skipping proxy %s, Timeout Exception" % proxy)
                self.proxy_dead.append(proxy)

            except requests.ConnectionError:
                self.logger.warning("Skipping proxy %s, ConnectionError Exception" % proxy)
                self.proxy_dead.append(proxy)

            except Exception as ex:
                self.logger.error("Exception by proxy %s occured! %s" % (proxy, str(ex)))
                self.proxy_dead.append(proxy)


if __name__ == '__main__':
    grabber = ProxyGrabber()
    proxyChecker = ProxyChecker(timeout=1)
    proxyChecker.run(size=5, proxies=grabber.get_proxies(limit=5))
    up = proxyChecker.get_proxies_up()
    print(up)
    dead = proxyChecker.get_proxies_dead()
    print(dead)
    sleep(5)
    proxyChecker.restart(size=5, proxies=grabber.get_proxies(limit=5))
    up = proxyChecker.get_proxies_up()
    print(up)
    dead = proxyChecker.get_proxies_dead()
    print(dead)