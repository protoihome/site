#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
from wiringx86 import GPIOGalileoGen2 as GPIO


class Dicionario(dict):
	def __init__(self):
		self = dict()

	def add(self, key, value):
		self[key] = value

class Device(object):
	def __init__(self):
		self.gpio = GPIO(debug=False)

	def OnDevice(self, pin_):
		return self.gpio.digitalWrite(pin_, self.gpio.HIGH)

	def offDevice(self, pin_):
		return self.gpio.digitalWrite(pin_, self.gpio.LOW)
