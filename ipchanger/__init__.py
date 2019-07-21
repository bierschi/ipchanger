__title__ = "ipchanger"
__version_info__ = ('1', '0', '0')
__version__ = ".".join(__version_info__)
__author__ = "Christian Bierschneider"
__email__ = "christian.bierschneider@web.de"
__license__ = "MIT"

# set library modules
from ipchanger.tor.tor import Tor
from ipchanger.utils.ip_analyzer import IPAnalyzer
from ipchanger.utils.logger import Logger