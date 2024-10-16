#
# modules/gui/upload_view.py
#

from threading import Thread
from time import sleep
import tkinter as tk
from tkinter import ttk

from .thread_control import THREAD_CONTROL, THREAD_SLEEP
from modules.queue.upload_queue import UploadQueue

class UploadView():
    __columns = ('id', 'Filename', 'File Size', 'User', 'Status', 'Rate', 
                 'Progress', 'Time Left' )

    __columns_width = ({'id': 20}, {'Filename': 210}, {'File Size': 100}, 
                       {'User': 100}, {'Status': 110}, {'Rate': 100}, 
                       {'Progress': 150}, {'Time Left': 120})   

    __main_window = None    
    __upload_treeview = None
    __frame = None
    
    def __init__(self, main_window):
        self.__main_window = main_window

        self.__frame = tk.Frame(self.__main_window)
        self.__frame.place(x=1, y=270, relwidth=1, height=200)

        self.__upload_treeview = ttk.Treeview(self.__frame,
                                              show='headings',
                                              column=self.__columns)    
    
    def __update_screen(self, db_upload_list: list):        
        # Check if the Treeview is empty.
        if not self.__upload_treeview.get_children():
            for db_upload_item in db_upload_list:
                self.__upload_treeview.insert('', tk.END, values=db_upload_item)
        else:
            # Update the Treeview.
            for db_upload_item in db_upload_list:
                db_id = db_upload_item[0]
                
                for treeview_item_id in self.__upload_treeview.get_children():
                    treeview_item_values = self.__upload_treeview.item(treeview_item_id)['values']                    
                    treeview_item_db_id = treeview_item_values[0]                    

                    if treeview_item_db_id == db_id:
                        self.__upload_treeview.item(treeview_item_id, values=db_upload_item)
                        break                                         
                else:
                    self.__upload_treeview.insert('', tk.END, values=db_upload_item)
    
    def __thread_loop(self):
       upload_queue = UploadQueue()
        
       while THREAD_CONTROL['transfer']:
           upload_list = upload_queue.list()            
           self.__main_window.after(0, self.__update_screen, upload_list)

           sleep(THREAD_SLEEP)
    
    def show(self):
        for column_data in self.__columns_width:
            for name, width in column_data.items():
                self.__upload_treeview.heading(name, text=name, anchor=tk.CENTER)

                # Don't centralize the Filename column.
                if name == 'Filename':                
                    self.__upload_treeview.column(name, width=width)                    
                else:
                    self.__upload_treeview.column(name, width=width,
                                                  anchor=tk.CENTER)
        
        y_scroll = tk.Scrollbar(self.__frame, orient='vertical', 
                                command=self.__upload_treeview.yview)

        self.__upload_treeview.configure(yscroll=y_scroll.set)
        y_scroll.pack(side='right', fill='y')

        x_scroll = tk.Scrollbar(self.__frame, orient='horizontal',
                                command=self.__upload_treeview.xview)

        self.__upload_treeview.configure(xscroll=x_scroll.set)
        x_scroll.pack(side='bottom', fill='x')

        self.__upload_treeview.pack(expand=True, fill='both')

        # Thread to update the download list.
        thread = Thread(target=self.__thread_loop)
        thread.daemon = True
        thread.start()