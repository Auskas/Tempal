#! /usr/bin/python3
# tempal.py - a simple python script for monitoring RPI GPU temperature.

import os, platform
import time
from tkinter import *
import logging

class TempWidget:

    def __init__(self,frame):
        self.logger = logging.getLogger('Tempal')
        self.logger.setLevel(logging.DEBUG)
        logFileHandler = logging.FileHandler('tempal_log.txt')
        logFileHandler.setLevel(logging.DEBUG)
        formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logFileHandler.setFormatter(formatterFile)
        self.logger.addHandler(logFileHandler)
        self.logger.info('########## SCRIPT STARTED ##########')
        
        self.FONT_SIZE = 20
        self.REFRESH_RATE = 1000 # temp refresh rate in milliseconds
        self.THRESHOLD = 60 # temp threshold in degrees Celcius
        
        self.messageMsg = Message(frame,  text='', fg='black', bg='black', font=("SFUIText", self.FONT_SIZE, "bold"), width=25 * self.FONT_SIZE)
        self.messageMsg.place(relx=0.5, rely=0.35, anchor=CENTER)
        self.measure_temp()

    def measure_temp(self):
        temp_GPU = os.popen("vcgencmd measure_temp").readline()
        try:
            temp_string_GPU = temp_GPU[temp_GPU.find('=') + 1: temp_GPU.find("'")]
            temp_float_GPU = float(temp_string_GPU)
            if temp_string_GPU.find("'C") != -1:
            	temp_formatted_GPU = f'GPU {temp_string_GPU}°C'
            else:
            	temp_formatted_GPU = f'GPU {temp_string_GPU}°F'
            self.messageMsg.config(text=temp_formatted_GPU)
            if temp_float_GPU < self.THRESHOLD:
                self.messageMsg.config(fg='green')
            else:
                self.messageMsg.config(fg='red')
            self.messageMsg.after(self.REFRESH_RATE, self.measure_temp)
        except Exception as exc:
            self.logger.error(f'The following error occured: {exc}')

window = Tk()
window.title('Tempal - RPI temperature monitor')
window.configure(bg='black')
# Disables closing the window by standard means, such as ALT+F4 etc.
# window.overrideredirect(True)
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w // 3, h // 3))
tempWidget = TempWidget(window)
window.mainloop()
