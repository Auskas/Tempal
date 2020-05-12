#! /usr/bin/python3
# settings.py - a simple GUI for Tempal - RPI temperature monitor.

import os, platform
import time
from tkinter import *
import logging
import json

class TempalSettings:
	def __init__(self,mainframe):
		self.MIN_TH_TEMP = int(50)
		self.MAX_TH_TEMP = int(85)
		
		if __name__ == '__main__':
			self.window = Tk()
		else:
			self.tempWidget = mainframe
			self.mainframe = mainframe.frame
			self.window = Toplevel(self.mainframe)
		self.window.title('Tempal - RPI temperature monitor settings')
		self.window.configure(bg='white')
		
		# Disables closing the window by standard means, such as ALT+F4 etc.
		# window.overrideredirect(True)
		w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
		self.window.geometry("%dx%d+0+0" % (w // 3, h // 3))
		#self.window.minsize(w // 3, h // 3)
		#self.window.maxsize(w // 2, h // 2)
		if __name__ == '__main__':
			self.FONT_SIZE = 12
			self.refresh_rate_value = 1000
			self.scale_value = 'Celsius'
			self.threshold_value = 85
		else:
			self.FONT_SIZE = mainframe.FONT_SIZE
			self.refresh_rate_value = mainframe.REFRESH_RATE
			self.threshold_value = mainframe.THRESHOLD
			self.scale_value = mainframe.SCALE
		
		self.temperature_scale_label = Label(self.window,
											 font=f'Default {self.FONT_SIZE}',
											 text='   Temperature threshold scale   ',
											 bg='white'
											 )
		self.temperature_scale_label.grid(row=0,column=0,sticky='e')
		
		self.temperature_scale_buttons = Frame(self.window,bg='white')
		self.temperature_scale_buttons.grid(row=0,column=1,sticky='w')
		
		var = StringVar()

		self.celsius_button=Radiobutton(self.temperature_scale_buttons,
										text='°C',
										variable=var,
										value='Celsius',
										bg='grey89',
										command=self.scale_change_celsius)
										
		self.fahrenheit_button=Radiobutton(self.temperature_scale_buttons,
										   text='°F',
										   variable=var,
										   value='Fahrenheit',
										   bg='grey89',
										   command=self.scale_change_fahrenheit)
										   
		self.celsius_button.grid(row=0,column=0)
		self.fahrenheit_button.grid(row=0,column=1)
		
		
		self.threshold_label = Label(self.window,
									 font=f'Default {self.FONT_SIZE}',
									 text='   Temperature threshold value   ',
									 bg='white'
									 )
		self.threshold_label.grid(row=1,column=0,sticky='e')

		self.threshold_slider = Scale(self.window,
							orient=HORIZONTAL,
							length=w // 6,
							from_=self.MIN_TH_TEMP,
							to=self.MAX_TH_TEMP,
							resolution=1,
							bg='white',
							activebackground='grey89',
							bd=0,
							command=self.threshold_change,
							)
							
		self.threshold_slider.set(self.threshold_value)
		self.threshold_slider.grid(row=1,column=1)
		
		self.refresh_rate_label = Label(self.window,
										font=f'Default {self.FONT_SIZE}',
										text='   Measurement rate, seconds   ',
										bg='white'
										)
		self.refresh_rate_label.grid(row=2,column=0,sticky='e')
		self.refresh_rate_entry = Entry(self.window,
										width=10,
										)
		self.refresh_rate_entry.insert(0,str(self.refresh_rate_value))
		self.refresh_rate_entry.grid(row=2,column=1,sticky='w')
		
		
		self.buttons = Frame(self.window, bg='white')
		self.buttons.grid(row=8,column=1,sticky='w')
		
		BUTTON_WIDTH = 4
		BUTTON_HEIGHT = 1
		self.apply_button = Button(self.buttons, 
								   text='Apply',
								   width=BUTTON_WIDTH,
								   height=BUTTON_HEIGHT,
								   font=f'default {self.FONT_SIZE}',
								   bg='grey89',
								   command=self.apply_button_pressed
								   )
		self.apply_button.grid(row=0,column=0)

		self.save_button = Button(self.buttons, 
								   text='Save & Exit',
								   width=int(BUTTON_WIDTH*1.8),
								   height=BUTTON_HEIGHT,
								   font=f'default {self.FONT_SIZE}',
								   bg='grey89',
								   command=self.save_button_pressed
								   )
		self.save_button.grid(row=0,column=1)		
    	
		self.cancel_button = Button(self.buttons, 
								   text='Cancel',
								   width=BUTTON_WIDTH,
								   height=BUTTON_HEIGHT,
								   font=f'default {self.FONT_SIZE}',
								   bg='grey89',
								   command=self.cancel_button_pressed
								   )
		self.cancel_button.grid(row=0,column=2)					   
		
		self.celsius_button.select() # Celsius temperature scale is default.
		if __name__ == '__main__':
			self.window.mainloop()

	def threshold_change(self,value):
		self.threshold_value = int(value)
		
	def scale_change_celsius(self):
		if self.scale_value == 'Fahrenheit':
			self.scale_value = 'Celsius'
			self.threshold_slider.config(from_=self.MIN_TH_TEMP,to=self.MAX_TH_TEMP)
			self.threshold_value = int((self.threshold_value - 32) / 1.8)
			self.threshold_slider.set(self.threshold_value)
		
	def scale_change_fahrenheit(self):
		if self.scale_value == 'Celsius':
			self.scale_value = 'Fahrenheit'
			self.threshold_value = int(self.threshold_value * 1.8 + 32)
			self.threshold_slider.config(from_=int(self.MIN_TH_TEMP * 1.8 + 32),to=int(self.MAX_TH_TEMP * 1.8 + 32))
			self.threshold_slider.set(self.threshold_value)
		
	def apply_button_pressed(self):
		if __name__ == '__main__':
			pass
		else:
			self.save_to_file()
			self.tempWidget.THRESHOLD = self.threshold_value
			self.tempWidget.SCALE = self.scale_value
			self.tempWidget.FONT_SIZE = self.FONT_SIZE
			try:
				self.tempWidget.REFRESH_RATE = int(self.refresh_rate_entry.get()) * 1000
			except Exception as exc:
				print(f'Cannot apply the refresh rate: {exc}')
	
	def save_button_pressed(self):
		if __name__ == '__main__':
			self.window.destroy()
		else:
			self.tempWidget.THRESHOLD = self.threshold_value
			self.tempWidget.SCALE = self.scale_value
			self.tempWidget.FONT_SIZE = self.FONT_SIZE
			try:
				self.tempWidget.REFRESH_RATE = int(self.refresh_rate_entry.get()) * 1000
			except Exception as esc:
				print(f'Cannot save the refresh rate: {exc}')
			self.save_to_file()
			self.window.destroy()
		
	def cancel_button_pressed(self):
		self.window.destroy()
		
	def save_to_file(self):
		try:
			with open('.tempal_settings.txt', 'w') as settings_file:
				settings = {
						    'FONT_SIZE': self.FONT_SIZE,
						    'REFRESH_RATE': self.refresh_rate_value,
							'SCALE': self.scale_value,
							'THRESHOLD': self.threshold_value
							}
				json.dump(settings, settings_file)
		except Exception as exc:
			print(f'Something went wrong: {exc}')
		

if __name__ == '__main__':
	mainframe = None
	settings = TempalSettings(mainframe)
