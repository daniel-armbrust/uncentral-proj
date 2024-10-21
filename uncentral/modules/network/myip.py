#
# modules/network/myip.py
#

import re
import random
from time import sleep
from threading import Thread

from modules.config import APP_DIRS, HTTP_ADDR_LOOKUP, MY_INFO_TABLE
from modules.config import THREAD_SLEEP_DISCOVERY_MY_IP
from modules.db.database import Database
from modules.utils import http_get


def remove_html_tags(html: str):
    """Remove HTML tags from a string.

    """
    clean = re.compile('<.*?>')    

    try:
        return re.sub(clean, '', html)
    except TypeError:
        return None
    

def extract_ip_address(text: str):
    """Extract an IP address from a string.
    
    """
    ip_addr = None

    # Regular expression pattern for matching IPv4 addresses.
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    if text:            
        ip_addr = re.search(ip_pattern, text).group()    

    return ip_addr
    

def get_my_ipaddr():
    """Get my own external, routable IP address. My own external address
    will try to be get from some external web servers.
    
    """
    ip_addr = None
        
    # Randomly get a web server from the list.
    host = random.choice(list(HTTP_ADDR_LOOKUP.keys()))
    port_list = HTTP_ADDR_LOOKUP[host]

    for port in port_list:
        # The first attempt will be through HTTP. After, HTTPS.
        http_resp = http_get(host=host, port=port)      

        if http_resp:
            text_resp = remove_html_tags(html=http_resp)
            ip_addr = extract_ip_address(text_resp)                    
            break

    return ip_addr


def discovery_thread():
    """
    
    """
    db_dir = APP_DIRS['db']
    db_filename = f'{db_dir}/peers.db'

    db = Database()
    db.filename = db_filename
    db.create(MY_INFO_TABLE)

    while True:
        my_ip = get_my_ipaddr()
                    
        if my_ip:
           sql = f'''
               INSERT OR REPLACE INTO my_info (id, ipv4) VALUES (1, "{my_ip}");               
           '''

           db.add(sql)

           sleep(THREAD_SLEEP_DISCOVERY_MY_IP)    


def start_myip_discovery():
    thread = Thread(target=discovery_thread)
    thread.daemon = True
    thread.start()