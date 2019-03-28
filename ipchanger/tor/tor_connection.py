import subprocess
import requests
from time import sleep
from stem import Signal
from stem.control import Controller


class TorConnection:
    """class TorConnection to set up a connection to the tor network

    USAGE:
            TorConnection(password='your_password', address='127.0.0.1')
    """

    def __init__(self, password, address, port=9051, http_proxy=None):
        """creates a TorConnection instance

        :param password: tor password for authentication
        :param address: tor host address
        :param port:  tor port communication
        :param http_proxy:
        """

        self.__password = password
        self.__address = address
        self.__port = port

        if http_proxy is None:
            self.http_proxy = "http://127.0.0.1:8118"
        else:
            self.http_proxy = http_proxy

        self.ip_request_str = "http://icanhazip.com/"
        self.real_host_ip = requests.get(self.ip_request_str).text

        self.__used_ips = list()

        if not self.__check_daemon():
            raise Exception

    def __check_daemon(self):
        """checks if tor daemon is running

        :return: Boolean: True if active
                          False if inactive
        """

        p = subprocess.Popen(["systemctl", "is-active", "tor"], stdout=subprocess.PIPE)

        out, err = p.communicate()

        if out.decode().rstrip() == 'active':
            print("Tor service is active")
            return True
        else:
            print("Tor service is inactive")
            return False

    def __trigger_new_ip(self):
        """triggers a new ip address, means not that current ip has changed!!

        """

        with Controller.from_port(address=self.__address, port=self.__port) as controller:
            controller.authenticate(password=self.__password)
            controller.signal(Signal.NEWNYM)
            sleep(1)

    def get_used_ips(self):
        """get list with all ip addresses

        :return: list: containing all used ip addresses
        """
        return self.__used_ips

    def get_current_ip(self):
        """get current ip address with request to icanhazip service

        :return: String: current ip address
        """

        current_ip = requests.get(url=self.ip_request_str, proxies={'http': self.http_proxy}).text.rstrip()
        self.save_used_ips(ip_address=current_ip)

        return current_ip

    def save_used_ips(self, ip_address):
        """save already used ip addresses in a list

        """
        if ip_address not in self.__used_ips:
            self.__used_ips.append(ip_address)

    def renew_ip(self):
        """renew current ip address, this can take a while

        :return: string, new ip address
        """

        old_ip = new_ip = self.get_current_ip()

        while old_ip == new_ip:

            old_ip = new_ip
            self.__trigger_new_ip()
            new_ip = self.get_current_ip()

        print("renewed the ip address to: %s" % (new_ip))

        return new_ip


if __name__ == '__main__':

    tor = TorConnection(password='', address='127.0.0.1', port=9051)

    for i in range(0, 2):
        print("new_ip: %s" % tor.renew_ip())

    print(tor.get_used_ips())
