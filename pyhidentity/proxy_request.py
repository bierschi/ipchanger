import logging
from pyhidentity.base_request import BaseRequest


class ProxyRequest(BaseRequest):
    """class ProxyRequest to make a request with proxy

    USAGE:
            proxyreq = ProxyRequest()
            proxyreq.get(url="http://icanhazip.com/")
    """
    def __init__(self, http_proxy=None, https_proxy=None):
        self.logger = logging.getLogger('pyhidentity')
        self.logger.info('create class ProxyRequest')

        # init base request class
        super().__init__()

    def new_identity(self):
        """

        :return:
        """
        pass

    def get(self, url, **kwargs):
        """ sends a get request

        :param url: url for the request
        :param kwargs: optional arguments
        :return: Response object
        """
        return self.session.get(url=url, **kwargs)

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
    print(proxyreq.get(url="http://icanhazip.com/").text)
