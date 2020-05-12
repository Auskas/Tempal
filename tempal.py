#! /usr/bin/python3
# tempal.py - a simple python script for monitoring RPI GPU temperature.

import os, platform
import time
from tkinter import *
import logging
import json
from settings import TempalSettings

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
        
        BUTTON_WIDTH = 4
        BUTTON_HEIGHT = 1
        
        try:
            with open('.tempal_settings.txt', 'r') as settings_file:
                settings = json.load(settings_file)
                self.FONT_SIZE = settings['FONT_SIZE']
                self.REFRESH_RATE = settings['REFRESH_RATE']
                self.THRESHOLD = settings['THRESHOLD']
                self.SCALE = settings['SCALE']
        except Exception as exc:
            print(f'Cannot get the settings: {exc}')
            print('Using defaults')
            self.FONT_SIZE = 12
            self.REFRESH_RATE = 1000 # temp refresh rate in milliseconds
            self.SCALE = 'Celsius'
            self.THRESHOLD = 85 # temp threshold in degrees Celcius

        self.frame= frame

        
        self.message_GPU_temp = Message(self.frame, 
                                  text='', 
                                  bg='white', 
                                  font=('Default', int(self.FONT_SIZE * 1.2), 'bold'), 
                                  width=25 * self.FONT_SIZE
                                  )
        self.message_GPU_temp.grid(row=0,column=0,sticky='w')
        self.measure_temp()
        
        self.message_CPU_temp = Message(self.frame,
                                        text='',
                                        bg='white',
                                        font=('Default', int(self.FONT_SIZE * 1.2), 'bold'),
                                        width=25 * self.FONT_SIZE
                                        )
        self.message_CPU_temp.grid(row=1,column=0,sticky='w')
        
        self.buttons_frame = Frame(self.frame, bg='white')
        self.buttons_frame.grid(row=2,column=0)
        
        self.settings_button = Button(self.buttons_frame, 
                                      text='Settings', 
                                      width=int(BUTTON_WIDTH*1.8),
                                      height=BUTTON_HEIGHT,
                                      bg='grey81',
                                      font=f'default {self.FONT_SIZE}',
                                      command=self.call_settings
                                      )
        self.settings_button.grid(row=0,column=0,sticky='w')
        
        self.quit_button = Button(self.buttons_frame, 
                                  text='Quit', 
                                  width=int(BUTTON_WIDTH*1.8),
                                  height=BUTTON_HEIGHT,
                                  bg='grey81',
                                  font=f'default {self.FONT_SIZE}',
                                  command=self.quit_button_pressed
                                      )
        self.quit_button.grid(row=0,column=1,sticky='w')
        
    def call_settings(self):
        settings_window = TempalSettings(tempWidget)
        
    def quit_button_pressed(self):
        self.frame.quit()
        
    def measure_temp(self):
        try:
            temp_GPU = os.popen("vcgencmd measure_temp").readline()
            temp_string_GPU = temp_GPU[temp_GPU.find('=') + 1: temp_GPU.find("'")]
            temp_float_GPU = float(temp_string_GPU)
            if self.SCALE == 'Celsius':
                temp_formatted_GPU = f'GPU {temp_string_GPU}°C'
            else:
                temp_float_GPU = round(temp_float_GPU * 1.8 + 32, 1)
                temp_formatted_GPU = f'GPU {str(temp_float_GPU)}°F'
                
            self.message_GPU_temp.config(text=temp_formatted_GPU)
            if temp_float_GPU < self.THRESHOLD:
                self.message_GPU_temp.config(fg='green')
            else:
                self.message_GPU_temp.config(fg='red')
            
        except Exception as exc:
            self.logger.error(f'The following error occured: {exc}')
            
        
        try:
            temp_CPU = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
            temp_float_CPU = round(int(temp_CPU) / 1000, 1)
            if self.SCALE == 'Celsius':
                temp_formatted_CPU = f'CPU {str(temp_float_CPU)}°C'
            else:
                temp_float_CPU = round(temp_float_CPU * 1.8 + 32, 1)
                temp_formatted_CPU = f'CPU {str(temp_float_CPU)}°F'
                
            self.message_CPU_temp.config(text=temp_formatted_CPU)
            if temp_float_CPU < self.THRESHOLD:
                self.message_CPU_temp.config(fg='green')
            else:
                self.message_CPU_temp.config(fg='red')
        except Exception as exc:
            self.logger.error(f'Cannot get the CPU temp: {exc}')
        
        self.message_GPU_temp.after(self.REFRESH_RATE, self.measure_temp)
            

#settings_window = TempalSettings()
window = Tk()
window.title('Tempal - RPI temperature monitor')
window.configure(bg='white')
# Disables closing the window by standard means, such as ALT+F4 etc.
# window.overrideredirect(True)
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w // 3, h // 3))
tempWidget = TempWidget(window)
window.mainloop()
