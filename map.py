#!/usr/bin/env python
# encoding: utf-8
"""
map.py

A class to generate points on a map within a restricted rectangle and determine drive time between 2 points.
This class uses the Google Maps API.
"""

import sys
import os
import unittest
import json
import urllib

class GoogleMaps:
	directionsAPI = "http://maps.googleapis.com/maps/api/directions/json?origin=%f,%f&destination=%f,%f&sensor=false"
	
	@staticmethod
	def toMiles(distance):
	    """Converts the API distance to miles"""
	    return float(distance)/1600
	
	@staticmethod
	def toMinutes(duration):
	    """Converts API duration to minutes"""
	    return float(duration)/60
	
	def __init__(self):
		pass
		
	def getDirections(self, pointA, pointB):
		"""Gets directions between two points"""
		try:
			response = json.load(urllib.urlopen(GoogleMaps.directionsAPI % (pointA[:2] + pointB[:2])))
			if( response['status'] != u'OK' ): raise Exception('Problem occured!')
			
			response = response['routes'][0]['legs'][0]
			
			
			# Now return the useful info to us
			return {
						'duration': response['duration']['value'], 
						'fromAddress': response['start_address'],
						'toAddress': response['end_address'],
						'distance': response['distance']['value'],
						'toPoint': pointB
					}
			
		except Exception as e:
			print e
			
		except urllib.error.URLError as e:
			print e
		


class mapTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()