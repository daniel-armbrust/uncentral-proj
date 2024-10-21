#
# modules/network/discovery.py
#

from time import sleep
from threading import Thread

from modules.config import APP_DIRS, MY_INFO_TABLE, REMOTE_PEERS_TABLE
from modules.config import THREAD_SLEEP_DISCOVERY_MY_IP
from modules.db.database import Database
from modules.utils import get_my_ipaddr


class PeersDiscovery():    
    __my_ipv4_addr = None
    __my_ipv6_addr = None

    def __init__(self):               
        db_dir = APP_DIRS['DB_DIR']
        db_filename = f'{db_dir}/peers.db'

        self.__db = Database()
        self.__db.filename = db_filename
        self.__db.create(REMOTE_PEERS_TABLE)
    
    def __thread_loop(self):
        pass

    def start(self):
        pass
        #thread_my_ip = Thread(target=self.__thread_update_my_ip)
        #thread_my_ip.daemon = True
        #thread_my_ip.start()

        #thread = Thread(target=self.__thread_loop)
        #thread.daemon = True
        #thread.start()