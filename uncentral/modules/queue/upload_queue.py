#
# modules/queue/upload_queue.py
#

import os
import sqlite3

UPLOAD_QUEUE_TABLE = '''
    CREATE TABLE IF NOT EXISTS upload_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        file_size REAL NOT NULL,
        user TEXT TNOT NULL,
        status TEXT CHECK(status IN ('Uploading', 'Error', 'Canceled', 'Finish')) NOT NULL,
        rate REAL NOT NULL,
        progress REAL NOT NULL,
        time_left INTEGER NOT NULL);
'''

class UploadQueue():
    __db_filename = None

    def __init__(self):
        current_dir = os.getcwd()
        self.__db_filename = f'{current_dir}/db/upload_queue.db'

        if not os.path.exists(self.__db_filename):
            self.__create_db()
    
    def __create_db(self):
        conn = sqlite3.connect(self.__db_filename)

        cursor = conn.execute(UPLOAD_QUEUE_TABLE)
        conn.commit()

        cursor.close()
        conn.close()
    
    def list(self):
        sql = '''
            SELECT id, filename, file_size, user, status, rate, progress, 
                time_left
            FROM upload_queue WHERE status != 'Finish'
        '''

        conn = sqlite3.connect(self.__db_filename)

        cursor = conn.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()        

        cursor.close()
        conn.close()

        return rows