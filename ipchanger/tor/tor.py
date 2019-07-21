import requests
import logging
import os
import signal
from time import sleep
from tempfile import mkdtemp
from shutil import rmtree

from stem.process import launch_tor_with_config
from stem.util import term
from stem.control import Controller
from stem import Signal
from stem.util import system
from stem import SocketError

from tor.proxy_request import ProxyRequest


class Tor(ProxyRequest):
    """class Tor to set up a tor process

    USAGE:
            Tor(socks_port=9050, control_port=9051)
    """
    def __init__(self, socks_port=9050, control_port=9051, http_proxy='127.0.0.1:8118', https_proxy='127.0.0.1:8118'):
        """

        :param socks_port: define socks port, default 9050
        :param control_port: define control port, default 9051
        """
        ProxyRequest.__init__(self)
        self.logger = logging.getLogger('ipchanger')
        self.logger.info('create class Tor')

        self.socks_port = socks_port
        self.control_port = control_port

        self.config = dict()
        self.process = None
        self.controller = None
        self.pid = None

        if http_proxy:
            self.proxies['http'] = http_proxy
        if https_proxy:
            self.proxies['https'] = https_proxy
        else:
            self.proxies = self.tor_default_proxies

        self.ip_request_str = "http://icanhazip.com/"
        self.real_host_ip = requests.get(self.ip_request_str).text
        self.logger.info('real host ip: %s' % self.real_host_ip)

        self.__used_ips = list()

        self.data_directory = mkdtemp()

    def __del__(self):
        """destructor
        """

        self.kill_process()

        if os.path.exists(self.data_directory):
            rmtree(self.data_directory)

    def request(self, url):
        """requests the given url

        """

        self.logger.info("request url: %s with proxy: %s" % (url, self.proxies['http']))
        self.session.proxies = self.proxies
        self.session.get(url=url)

    def launch(self, exit_nodes=None):
        """launches a tor process with configuration dictionary

        :return: self object
        """

        if exit_nodes is None:
            pid = self.__get_tor_pid()
            if pid is None:
                self.logger.info("starting tor process with default configuration")

                try:
                    self.process = launch_tor_with_config(
                        config=self.__create_config(),
                        init_msg_handler=self.__print_bootstrap_lines,
                    )
                except OSError as ex:
                    self.logger.error(ex)
                except (ConnectionRefusedError, SocketError) as ex:
                    self.logger.error(ex)

            else:
                self.logger.info("tor process is already running with pid %d" % pid)

        else:
            self.kill_process()
            self.logger.info("starting tor process with defined exit nodes %s" % exit_nodes)

            try:
                self.process = launch_tor_with_config(
                    config=self.__create_config(exit_nodes=exit_nodes),
                    init_msg_handler=self.__print_bootstrap_lines,
                )
            except OSError as ex:
                self.logger.error(ex)
            except (ConnectionRefusedError, SocketError) as ex:
                self.logger.error(ex)

        self.controller = Controller.from_port(port=self.control_port)
        self.controller.authenticate()

        return self

    def restart(self, exit_nodes=None):
        """restart the tor process

        :param exit_nodes: str with country codes in form: '{gb}, {ru}, {us}'
        """
        self.logger.info("restart tor process")
        self.kill_process()
        self.__used_ips = list()
        self.launch(exit_nodes=exit_nodes)

    def kill_process(self):
        """kills current tor process

        """

        pid = self.__get_tor_pid()

        if pid is not None:
            if self.controller is not None:
                self.controller.close()
            os.kill(pid, signal.SIGKILL)
            self.logger.info("killed tor process with pid %d" % pid)
        else:
            self.logger.info("pid for tor process not found!")

    def __get_tor_pid(self):
        """get current tor process id

        :return: int, pid
        """
        pid = system.pid_by_port(self.socks_port)

        if pid is None:
            pid = system.pid_by_name('tor')

        return pid

    def __create_config(self, exit_nodes=None):
        """creates a config dictionary

        :param exit_nodes: str with country codes in form: '{gb}, {ru}, {de}, {us}'
        :return: dict, configuration settings
        """
        # default config
        self.config.update({

            "SOCKSPort": str(self.socks_port),
            "ControlPort": str(self.control_port),
            "DataDirectory": self.data_directory,
            "ExitRelay": str(0),
        })

        if exit_nodes is not None:
            if isinstance(exit_nodes, str):

                self.config.update({

                    "ExitNodes": exit_nodes

                })
            else:
                raise TypeError("'exit_nodes' must be type of string in form: '{us}, {ru}, {de}'")

        return self.config

    def __print_bootstrap_lines(self, line):
        """sets up a msg handler for init

        :param line: logger output
        """
        if "Bootstrapped" in line:
            self.logger.debug("Tor logger outputs: %s" % line)
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
            self.logger.error("Exception while trying to trigger new ip: %s" % ex)

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
        try:

            current_ip = requests.get(url=self.ip_request_str, proxies=self.proxies).text.rstrip()
            self.__save_used_ips(ip_address=current_ip)

            return current_ip

        except ConnectionRefusedError as ex:
            self.logger.error("ConnectionRefusedError: %s" % ex)

    def renew_ip(self):
        """renew current ip address, this can take a while

        :return: string, new ip address
        """

        old_ip = new_ip = self.get_current_ip()

        while old_ip == new_ip:

            old_ip = new_ip
            self.__trigger_new_ip()
            new_ip = self.get_current_ip()

        self.logger.info("renewed the ip address to: %s" % new_ip)

        return new_ip


if __name__ == '__main__':
    tor = Tor(socks_port=9050, control_port=9051).launch()


