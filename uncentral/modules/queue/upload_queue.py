#
# modules/queue/upload_queue.py
#

from modules.config import APP_DIRS, UPLOAD_QUEUE_TABLE
from modules.db.database import Database


class UploadQueue():    
    def __init__(self):                       
        db_filename = f"{APP_DIRS['db']}/upload_queue.db"
        
        self.__db = Database()
        self.__db.filename = db_filename
        self.__db.create(UPLOAD_QUEUE_TABLE)
    
    def list(self):
        sql = '''
            SELECT id, filename, file_size, user, status, rate, progress, 
                time_left
            FROM upload_queue WHERE status != 'Finish'
        '''

        rows = self.__db.list(sql)

        return rows
    
    def get(self):
        pass    
    
    def add_uploading(self, filename: str, tmp_filename: str):
        sql = f'''
            INSERT INTO upload_queue (filename, tmp_filename, status)
                VALUES ("{filename}", "{tmp_filename}", "Downloading")
        '''

        row_id = self.__db.create(sql)

        return row_id
    
    def update_completed(self, id: int):
        sql = f'''
            UPDATE upload_queue SET status = "Completed" WHERE id = "{id}"                            
        '''

        self.__db.update(sql)