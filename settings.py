#! /usr/bin/python3
# settings.py - a simple GUI for Tempal - RPI temperature monitor.

import os, platform
import time
from tkinter import *
import logging

class TempalSettings:
	def __init__(self): 
		self.window = Tk()
		self.window.title('Tempal - RPI temperature monitor settings')
		self.window.configure(bg='white')
		# Disables closing the window by standard means, such as ALT+F4 etc.
		# window.overrideredirect(True)
		w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
		self.window.geometry("%dx%d+0+0" % (w // 3, h // 3))

		self.threshold_value = 0
		self.threshold_label = Label(self.window,text='Temperature threshold value',bg='white')
		self.threshold_label.grid(row=0,column=0)

		self.slider = Scale(self.window,
							orient=HORIZONTAL,
							length=300,
							from_=0,
							to=100,
							resolution=1,
							bg='white',
							activebackground='grey',
							bd=0,
							command=self.threshold_change,
							)
		self.slider.set(70)
		self.slider.grid(row=0,column=1)
		self.window.mainloop()

	def threshold_change(self,value):
		self.threshold_value = value
		print(self.threshold_value)

if __name__ == '__main__':
	settings = TempalSettings()