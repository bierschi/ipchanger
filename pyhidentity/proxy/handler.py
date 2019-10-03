import logging
import threading
from pyhidentity.proxy.grabber import ProxyGrabber
from pyhidentity.proxy.checker import ProxyChecker
from pyhidentity.db.proxy_db import ProxyDB
from time import sleep


class ProxyHandler:
    """class ProxyHandler to manage Proxies

    USAGE:
            ProxyHandler()
    """
    def __init__(self, timeout=1, daemon=False):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info("create class ProxyHandler")

        if isinstance(timeout, int):
            self.timeout = timeout
        else:
            raise TypeError("'timeout must be type of int!")

        # load proxy classes
        self.grabber = ProxyGrabber()
        self.checker = ProxyChecker(timeout=self.timeout)
        self.proxy_db = ProxyDB()

        self.__thread = threading.Thread(target=self.__run, daemon=daemon)
        self.__running = False

    def __del__(self):
        """

        :return:
        """
        self.stop()

    def start(self, daemon=False):
        """

        :return:
        """

        if self.__thread:
            self.logger.info("start proxy handler thread")
            if isinstance(daemon, bool):
                self.__thread.daemon = daemon
                self.__running = True
                self.__thread.start()

            else:
                self.logger.error("'daemon' must be type of boolean")
                raise TypeError("'daemon' must be type of boolean")

    def stop(self):
        """

        :return:
        """
        if self.__thread:
            self.logger.info("stop proxy handler thread")
            self.__running = False
            self.__thread.join()

    def __run(self):
        """

        :return:
        """

        while self.__running:
            print("test")

            proxies = self.grabber.get_proxies()
            self.checker.run(proxies=proxies, size=150)
            proxy_up = self.checker.get_proxies_up()
            proxy_dead = self.checker.get_proxies_dead()
            print(proxy_up)
            sleep(20)

if __name__ == '__main__':
    handler = ProxyHandler()
    handler.start(daemon=False)
    sleep(300)
    handler.stop()


