#
# modules/config.py
#

APP_DIRS = {'tmp': '', 'share': '', 'db': ''}

THREAD_CONTROL = {
    'home': False, 
    'chat': False, 
    'library': False,
    'search': False, 
    'transfer': False
}

THREAD_SLEEP = 2

# Sleep time in seconds for discovery of my own IP Address.
THREAD_SLEEP_DISCOVERY_MY_IP = 300

DOWNLOAD_QUEUE_TABLE = '''
    CREATE TABLE IF NOT EXISTS download_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        tmp_filename TEXT NOT NULL,
        file_size REAL DEFAULT 0,
        user TEXT DEFAULT 'Unknown',
        status TEXT CHECK(status IN ('Downloading', 'Getting Info', 'Error', 'Canceled', 'Completed')) NOT NULL,
        rate REAL DEFAULT 0,
        progress REAL DEFAULT 0,
        time_left INTEGER);
'''

UPLOAD_QUEUE_TABLE = '''
    CREATE TABLE IF NOT EXISTS upload_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        file_size REAL DEFAULT 0,
        user TEXT DEFAULT 'Unknown',
        status TEXT CHECK(status IN ('Uploading', 'Error', 'Canceled', 'Finish')) NOT NULL,
        rate REAL DEFAULT 0,
        progress REAL DEFAULT 0,
        time_left INTEGER NOT NULL DEFAULT 0);
'''

REMOTE_PEERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS peer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ipv4 TEXT NOT NULL UNIQUE);
'''

# Table to record my own external, routable IP address. 
MY_INFO_TABLE = '''
    CREATE TABLE IF NOT EXISTS my_info (
        id INTEGER PRIMARY KEY,
        ipv4 TEXT UNIQUE,
        ipv6 TEXT UNIQUE);
'''

# HTTP sites for try to obtain my own external address.
HTTP_ADDR_LOOKUP = {'checkip.dyndns.org': (80, 443,),
                    'ifconfig.me': (80, 443,)}