#
# uncentral.py
#

import sys
import tkinter as tk

from modules.gui.main_view import MainView
from modules.network.server import Server

def main():
    root_window = tk.Tk()
    root_window.title('Uncentral v1.0.0 BETA')
    root_window.geometry('1000x560')
    root_window.minsize(width=800, height=400)        
    
    main_view = MainView(root_window)    
    #uncentral_view.screen_loadapp()
    main_view.screen_transfer()

    server = Server()
    server.start()

    root_window.mainloop()

    sys.exit(0)


if __name__ == '__main__':
    main()
else:
    sys.exit(1)
