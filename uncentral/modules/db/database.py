#
# modules/db/database.py
#

import sqlite3

class Database():
    __conn = None
    __filename = None

    @property
    def filename(self):
        return self.__filename
    
    @filename.setter
    def filename(self, value: str):        
        self.__filename = value
        self.__conn = sqlite3.connect(self.__filename)          
   
    def __del__(self):
        try:
            self.__conn.close()
        except (sqlite3.Error, sqlite3.ProgrammingError,):
            pass
    
    def __select(self, sql: str):
        row = None
        
        cursor = self.__conn.execute(sql)
        row = cursor.fetchall()

        cursor.close()

        return row

    def __commit(self, sql: str):
        new_id = None   
        cursor = None     

        try:
            cursor = self.__conn.execute(sql)
            self.__conn.commit()

            new_id = cursor.lastrowid
        except sqlite3.Error as e:
            print(f'An error occurred: {e}')
            self.__conn.rollback()            
        
        if cursor:
            cursor.close()        
        
        return new_id        
    
    def create(self, ddl: str):        
        cursor = None

        try:
            cursor = self.__conn.execute(ddl)
        except sqlite3.Error as e:
            print(f'An error occurred: {e}')
        
        if cursor:
            cursor.close()

    def exec(self, sql: str):
        self.__commit(sql)
        
    def add(self, sql: str):
        new_id = self.__commit(sql)

        return new_id        

    def update(self, sql: str):
        new_id = self.__commit(sql)

        return new_id

    def delete(self, sql: str):
        new_id = self.__commit(sql)

        return new_id
    
    def list(self, sql: str):
        row = self.__select(sql)

        return row
        

        
