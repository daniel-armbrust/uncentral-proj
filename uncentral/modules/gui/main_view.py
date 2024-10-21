#
# modules/gui/main_view.py
#

import tkinter as tk

from .download_view import DownloadView
from .upload_view import UploadView
from modules.config import THREAD_CONTROL

class MainView():
    __main_window = None
    __main_frame = None     

    def __init__(self, main_window):
        self.__main_window = main_window

        self.__button_img_home = tk.PhotoImage(file='img/home-button-img.png')
        self.__button_img_chat = tk.PhotoImage(file='img/chat-button-img.png')
        self.__button_img_library = tk.PhotoImage(file='img/library-button-img.png')
        self.__button_img_search = tk.PhotoImage(file='img/search-button-img.png')
        self.__button_img_transfer = tk.PhotoImage(file='img/transfer-button-img.png')

        self.__menu_top()        
        self.__setup_frame()               
    
    def __stop_thread(self):
        for k,v in THREAD_CONTROL.items():
            THREAD_CONTROL[k] = False

    def __setup_frame(self):
        if self.__main_frame:
            for widget in self.__main_frame.winfo_children():
                widget.destroy()
        
        self.__main_frame = tk.Frame(self.__main_window)
        self.__main_frame.place(x=1, y=10, relwidth=1, relheight=1)

        self.__buttons_top()

    def __menu_top(self):
        menu_bar_top = tk.Menu(self.__main_window)
        menu_top = tk.Menu(menu_bar_top, tearoff=0)

        menu_top.add_cascade(label='File', menu=menu_bar_top)
        menu_top.add_cascade(label='Actions', menu=menu_bar_top)
        menu_top.add_cascade(label='Help', menu=menu_bar_top)

        self.__main_window.config(menu=menu_top)
        
    def __buttons_top(self):
        # Home        
        self.__button_home = tk.Button(self.__main_window,
                                       image=self.__button_img_home,
                                       command=self.screen_home)
        self.__button_home.place(x=2, y=5)
           
        # Chat        
        self.__button_chat = tk.Button(self.__main_window,
                                       image=self.__button_img_chat, 
                                       command=self.screen_chat)
        self.__button_chat.place(x=143, y=5)

        # Library        
        self.__button_library = tk.Button(self.__main_window, 
                                   image=self.__button_img_library, 
                                   command=self.screen_library)
        self.__button_library.place(x=283, y=5)

        # Search        
        self.__button_search = tk.Button(self.__main_window,
                                         image=self.__button_img_search, 
                                         command=self.screen_search)
        self.__button_search.place(x=423, y=5)

        # Transfer                
        self.__button_transfer = tk.Button(self.__main_window, 
                                           image=self.__button_img_transfer, 
                                           command=self.screen_transfer)
        self.__button_transfer.place(x=563, y=5)        

    def screen_loadapp(self):
        pass

    def screen_home(self):
        self.__setup_frame()        
        self.__stop_thread()

        THREAD_CONTROL['home'] = True

        self.__button_home.config(relief=tk.RIDGE)

    def screen_chat(self):
        self.__setup_frame()
        self.__stop_thread()

        THREAD_CONTROL['chat'] = True

        self.__button_chat.config(relief=tk.RIDGE)

    def screen_library(self):
        self.__setup_frame()
        self.__stop_thread()

        THREAD_CONTROL['library'] = True

        self.__button_library.config(relief=tk.RIDGE)

    def screen_search(self):
        self.__setup_frame()
        self.__stop_thread()

        THREAD_CONTROL['search'] = True

        self.__button_search.config(relief=tk.RIDGE)

    def screen_transfer(self):
        self.__setup_frame()
        self.__stop_thread()

        THREAD_CONTROL['transfer'] = True

        self.__button_transfer.config(relief=tk.RIDGE)

        download_view = DownloadView(self.__main_window)        
        download_view.show()

        upload_view = UploadView(self.__main_window)        
        upload_view.show()