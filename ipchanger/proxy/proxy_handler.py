from proxy.proxy_grabber import ProxyGrabber
from proxy.proxy_checker import ProxyChecker
from db.proxy_db import ProxyDB


class ProxyHandler:
    """class ProxyHandler to manage Proxies

    USAGE:
            ProxyHandler()
    """
    def __init__(self):

        # load proxy classes
        self.grabber = ProxyGrabber()
        self.checker = ProxyChecker()
        self.proxy_db = ProxyDB()

    def __del__(self):
        pass

    def run(self):
        pass


