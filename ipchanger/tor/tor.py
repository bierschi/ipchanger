import requests
import logging
from os import path
from time import sleep
from tempfile import mkdtemp
from shutil import rmtree

from stem.process import launch_tor_with_config
from stem.util import term
from stem.control import Controller
from stem import Signal
from ipchanger.tor.ip_analyzer import IPAnalyzer

logger = logging.getLogger(__file__)


class Tor:
    """class Tor to set up a tor process

    USAGE:
            Tor(socks_port=9050, control_port=9051)
    """
    def __init__(self, socks_port=9050, control_port=9051):
        """

        :param socks_port: define socks port, default 9050
        :param control_port: define control port, default 9051
        """

        self.logger = logging.getLogger(__file__)

        self.socks_port = socks_port
        self.control_port = control_port

        self.config = None
        self.process = None
        self.controller = None

        self.http_proxy = "http://127.0.0.1:8118"

        self.ip_request_str = "http://icanhazip.com/"
        self.real_host_ip = requests.get(self.ip_request_str).text
        self.__used_ips = list()

        self.data_directory = mkdtemp()

    def __del__(self):
        """destructor

        """
        self.controller.close()
        self.process.terminate()
        self.process.wait()

        if path.exists(self.data_directory):
            rmtree(self.data_directory)

    def launch(self):
        """

        :return:
        """
        self.process = launch_tor_with_config(
            config=self.create_default_cfg(),
            init_msg_handler=self.__print_bootstrap_lines,
        )

        self.controller = Controller.from_port(port=self.control_port)
        self.controller.authenticate()

        return self

    def kill_process(self):
        """kills current tor process

        """
        if self.process:
            self.logger.info("Killing tor process")
            self.process.kill()

    def create_default_cfg(self):
        """

        :return:
        """
        self.config = {

            "SOCKSPort": str(self.socks_port),
            "ControlPort": str(self.control_port),
            "DataDirectory": self.data_directory,
            "ExitRelay": str(0),
            "ExitNodes": '{ru}'
        }

        return self.config

    def update_cfg(self):
        """

        :return:
        """

        self.config.update({
            "ExitNodes": '{ru}'
        })

    def __print_bootstrap_lines(self, line):
        """

        :return:
        """
        if "Bootstrapped" in line:
            self.logger.debug("[%05d] Tor logger outputs: %s", self.socks_port, line)
            print(term.format(line, term.Color.BLUE))

        if "100%" in line:
            self.logger.debug("[%05d] Tor process executed successfully" % self.socks_port)

    def __trigger_new_ip(self):
        """triggers a new ip address, means not that current ip has changed!!

        """

        try:

            with self.controller as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                sleep(1)

        except Exception as ex:
            print("Exception while trying to trigger new ip: %s" % ex)

    def __save_used_ips(self, ip_address):
        """save already used ip addresses in a list

        """
        if ip_address not in self.__used_ips:
            self.__used_ips.append(ip_address)

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
        self.__save_used_ips(ip_address=current_ip)

        return current_ip

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
    tor = Tor(socks_port=9050, control_port=9051)
    p1 = tor.launch()
    i =0
    while i < 3:
        p1.renew_ip()
        sleep(2)
        i += 1
    print(p1.get_used_ips())
    p1.kill_process()