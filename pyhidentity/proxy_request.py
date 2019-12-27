import logging
from pyhidentity.base_request import BaseRequest


class ProxyRequest(BaseRequest):
    """class ProxyRequest to make a request with proxy

    USAGE:
            proxyreq = ProxyRequest()
            proxyreq.get(url="http://icanhazip.com/")
    """
    proxy_pool = dict()

    def __init__(self, proxytype='all'):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class ProxyRequest')

        # init base request class
        super().__init__()

    def new_identity(self):
        """

        :return:
        """
        self.index = random.randint(0, len(self.proxy_pool['http']) -1)
        tmp_proxy = self.proxy_pool['http'][self.index]
        print(tmp_proxy)
        self.proxies['http'] = tmp_proxy
        self.proxies['https'] = tmp_proxy
        self.session.proxies = self.proxies
        pass

    def get(self, url, **kwargs):
        """ sends a get request

        :param url: url for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        try:
            return self.session.get(url=url, proxies=self.proxies, timeout=1, **kwargs)
        except Exception as e:
            print(e)
            self.new_identity()
            self.get(url=url)
        #return self.session.get(url=url, proxies=self.proxies, timeout=1, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """ sends a post request

        :param url: url for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        return self.session.post(url=url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """ sends a put request

        :param url: url for the request
        :param data: data for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        return self.session.put(url=url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        """ sends a delete request

        :param url: url for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        return self.session.delete(url=url, **kwargs)


if __name__ == '__main__':
    proxyreq = ProxyRequest()
    resp = proxyreq.get(url="http://google.com")
    print(resp.content)
