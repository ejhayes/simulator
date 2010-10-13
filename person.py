#!/usr/bin/env python
# encoding: utf-8
"""
person.py

The types of people that can be used in a simulation (i.e. drivers and customers)
"""

import sys
import os
import unittest
import math
import random
from map import GoogleMaps

class person:
    """A generic person class.  Assumes that a person is only busy when they are going somewhere"""
    
    worldMap = GoogleMaps()
    
    def __init__(self, simulationClock, location):
        self.simulationClock, self.requestTime, self.location, self.busyUntil = simulationClock, simulationClock.getTime(), location, 0
    
    def isBusy(self):
        """Is this person busy?"""
        return self.simulationClock >= self.busyUntil
        
    def setBusy(self, duration):
        if self.isBusy():
            return False
        else:
            self.busyUntil = self.simulationClock.getTime() + duration
            return True        
    
    def calculateRoute(self, currentRoute, nextPoint):
        """
        Calculates a leg of a given trip
        """
        lat, lng, billable = range(3)

        if type(currentRoute) is not list:
            # first iteration
            currentRoute = [person.worldMap.getDirections(currentRoute, nextPoint)]
        else:
            currentRoute.append(person.worldMap.getDirections(currentRoute[-1]['toPoint'],nextPoint))
            
        # add the billing details (False by default)
        currentRoute[-1].update({'billable': nextPoint[billable] if len(nextPoint) is 3 else False})
        return currentRoute

    
    def calculateRouteFromItinerary(self, itinerary):
        """
        Calculates a trip based on a single pont or multiple points.  Assumes that the first point is where the person is.
        
        The itinerary can either look like:
        [(lat,lng,billable), (lat,lng,billable), ...]
        
        or:
        (lat, lng, billable)
        
        Where billable is a boolean used to determine whether to charge for a given leg of a trip.
        
        Returns a list that looks like this:
        [routeSummaryLeg1, routeSummaryLeg2, ...] where routeSummary is the object returned by the GoogleMaps getdirections function
        """
        
        # if we only supply one point
        if type(itinerary) is tuple:
            itinerary = [itinerary]
        
        # where we are is part of the itinerary
        itinerary.insert(0, self.location + (False,))
        
        # calculate the route
        return reduce(self.calculateRoute, itinerary)
            
    
class driver(person):
    pass


class customer(person):
		
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