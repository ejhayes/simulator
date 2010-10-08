#!/usr/bin/env python
# encoding: utf-8
"""
customer.py

A customer class
"""

import sys
import os
import unittest
import math
import random



class customer:
	def __init__(self, requestTime, route):
		# initialize parameters
		self.requestTime, self.route, = requestTime, route
		
	def startRide(self, startTime):
		self.startTime = startTime
		
	def finishRide(self, finishTime):
		"""
		Now that the ride is complete, get the details about it:
		- how long did the customer wait
		- what was the trip time
		- what is the customer rating
		- what is the driving rating
		- what is the fare
		"""
		
		return {
			tripTime: self.route['duration'],
			waitTime: self.startTime - self.requestTime,
			tripDistance: self.route['distance']
		
		}

class customerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()