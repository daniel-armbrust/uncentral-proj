#
# modules/network/server.py
#

import os
import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from modules import utils
from modules.queue.download_queue import DownloadQueue

class DaemonThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the daemon attribute for all threads in the pool
        for thread in self._threads:
            thread.daemon = True

class Server():
    __ip = '0.0.0.0'
    __port = 6699
    __max_connection = 5
    __share_dir = None
    __tmp_dir = None

    @property
    def ip(self):        
        return self.__ip
    
    @ip.setter
    def ip(self, value: str):                
        self.__ip = value
    
    @property
    def port(self):        
        return self.__port
    
    @port.setter
    def port(self, value: int):                
        self.__port = value
    
    @property
    def max_connection(self):        
        return self.__max_connection
    
    @port.setter
    def max_connection(self, value: int):                
        self.__max_connection = value
    
    def __init__(self):
        current_dir = os.getcwd()
        self.__share_dir = f'{current_dir}/share'
        self.__tmp_dir = f'{current_dir}/tmp'

    def __handle_transfer(self, client_socket, client_ip_addr):
        download_queue = DownloadQueue()

        with client_socket:            
            # Read the length of the filename (4 bytes)
            filename_length = client_socket.recv(4)

            if not filename_length:
                return            
            
            filename_length = int.from_bytes(filename_length, 'big')                          
            recv_filename = client_socket.recv(filename_length).decode('utf-8') 

            tmp_filename = utils.gen_tmp_filename(recv_filename) 
            tmp_filename_path = f'{self.__tmp_dir}/{tmp_filename}'

            download_id = download_queue.add_downloading(filename=recv_filename,
                                                         tmp_filename=tmp_filename)
            
            with open(tmp_filename_path, 'wb') as f:
                while True:
                    recv_data = client_socket.recv(1024) 
                    
                    if not recv_data:
                        break  

                    f.write(recv_data)
            
            # Move completed downloaded file from temp dir to shared dir.
            completed_filename_path = f'{self.__share_dir}/{recv_filename}'            
            utils.move_file(src=tmp_filename_path, dst=completed_filename_path)

            download_queue.update_completed(id=download_id)

    def __server_thread(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.__ip, self.__port))        
        server_socket.listen(self.__max_connection)

        print(f'Server listening on {self.__ip}:{self.__port}')

        with DaemonThreadPoolExecutor(max_workers=self.__max_connection) as exec:
            while True:
                client_socket, client_ip_addr = server_socket.accept()
                exec.submit(self.__handle_transfer, client_socket, client_ip_addr)
        
    def start(self):             
        thread = Thread(target=self.__server_thread)
        thread.daemon = True
        thread.start()