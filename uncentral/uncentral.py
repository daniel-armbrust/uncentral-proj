#
# uncentral.py
#

import os
import sys
import tkinter as tk

from modules.config import APP_DIRS
from modules.gui.main_view import MainView
from modules.network.server import Server
from modules.network.myip import start_myip_discovery


def create_app_dirs():
    """Create the application directories if it not exist.
    
    """
    global APP_DIRS

    current_dir = os.getcwd()
   
    for name, dir in APP_DIRS.items():
        app_dir = f'{current_dir}/{name}'
        APP_DIRS[name] = app_dir

        if not os.path.isdir(app_dir):
            os.mkdir(app_dir)

   
def main():
    create_app_dirs()    

    root_window = tk.Tk()
    root_window.title('Uncentral v1.0.0 BETA')
    root_window.geometry('1000x560')
    root_window.minsize(width=800, height=400)        
    
    main_view = MainView(root_window)    
    #uncentral_view.screen_loadapp()
    main_view.screen_transfer()

    # Function to keep discovering of my IP Address.
    start_myip_discovery()

    server = Server()
    server.start()   

    root_window.mainloop()

    sys.exit(0)


if __name__ == '__main__':
    main()
else:
    sys.exit(1)
