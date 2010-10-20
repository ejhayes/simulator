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
        # record keeping
        self.simulationClock, self.requestTime, self.location, self.busyUntil = simulationClock, simulationClock.getTime(), location, 0
    
        # personal stats
        self.stats = None
    
    def isBusy(self):
        """Is this person busy?"""
        return self.simulationClock >= self.busyUntil
        
    def setBusy(self, duration):
        if self.isBusy():
            return False
        else:
            self.busyUntil = self.simulationClock.getTime() + duration
            return True  
            
    def getLocation(self):
        """Returns the person current location"""
        return self.location
        
    def setLocation(self,location):
        self.location = location
    
    def calculateRoute(self, currentRoute, nextPoint):
        """
        Calculates a leg of a given trip
        """

        if type(currentRoute) is not list:
            # first iteration
            currentRoute = [person.worldMap.getDirections(currentRoute, nextPoint)]
        else:
            currentRoute.append(person.worldMap.getDirections(currentRoute[-1]['toPoint'],nextPoint))
            
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
        
        # returns the scheduled itinerary
        return reduce(self.calculateRoute, itinerary)
        
    def calculateRouteStats(self, route):
        """
        Returns a dictionary with the following information:
        - billableMiles
        - billableMinutes
        - nonBillableMiles
        - nonBillableMinutes
        """
        print route    
        ret = {}
        ret['totalMiles'] = GoogleMaps.toMiles(sum([i['distance'] for i in route]))
        ret['totalMinutes'] = GoogleMaps.toMinutes(sum([i['duration'] for i in route]))
        
        return ret
        
    def setRoute(self, itinerary):
        """
        Shortcut to calculate a route, determine the stats, set internal settings, and get busy!
        """
        stats = self.calculateRouteStats(self.calculateRouteFromItinerary(itinerary))
        self.setBusy(stats['totalMinutes'])
        self.setLocation(itinerary[-1])
        
        if self.stats is None:
            # stats haven't been set yet
            self.stats = stats
        else:
            # update the dictionary with the new stats
            self.stats = dict(zip(stats.keys(),map(sum,zip(self.stats.values(),stats.values()))))
            
        # end the call by returning route stats
        return stats
            
    def getStats(self):
        return self.stats
        
    
class driver(person):
    """
    Drivers do all the driving.  Default driver configuration values are based on San Francisco average taxi costs
    """
    
    counter = 0
    
    def __init__(self, simulationClock, location, initialFare=2.85, initialDistance=0.2, farePerMile=2.25):
        self.initialFare, self.initialDistance, self.farePerMile = initialFare, initialDistance, farePerMile
        
        # Give the driver a name
        self.name = driver.counter
        driver.counter += 1
        
        # initialize our super class (old style)
        person.__init__(self,simulationClock,location)

    def getName(self):
        """Returns sample driver name"""
        return 'Driver ' + str(self.name)
        

    def calculateFare(self, distance):
        if distance > self.initialDistance:
            rate = 0.0
            distance -= self.initialDistance
            rate += self.initialFare
            rate += distance * self.farePerMile
            return rate
        else:
            return self.initialFare
            
    def calculateRouteStats(self, route):
        ret = person.calculateRouteStats(self,route)
        
        # calculate the driver stats
        ret['billableMiles'] = GoogleMaps.toMiles(sum([i['distance'] for i in route if i['fare'] > 0]))
        ret['billableMinutes'] = GoogleMaps.toMinutes(sum([i['duration'] for i in route if i['fare'] > 0]))
        ret['nonBillableMiles'] = GoogleMaps.toMiles(sum([i['distance'] for i in route if i['fare'] == 0]))
        ret['nonBillableMinutes'] = GoogleMaps.toMinutes(sum([i['duration'] for i in route if i['fare'] == 0]))
        ret['totalFare'] = sum(i['fare'] for i in route)
            
        return ret
    
    def calculateRoute(self, currentRoute, nextPoint):
        """
        Calculates a leg of a given trip
        """
        if currentRoute is None:
            return []
            
        # positional args of nextPoint
        lat, lng, billable = range(3)
        
        currentRoute = person.calculateRoute(self, currentRoute, nextPoint)

        # add the fare
        currentRoute[-1].update({'fare': self.calculateFare(GoogleMaps.toMiles(currentRoute[-1]['distance'])) if nextPoint[billable] is True else 0})
        return currentRoute    
        

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

class cab:
    """
    The cab class
    """
    
    def __init__(self):
        self.queue = []
        
    def push(self,cabSet,toLocation):
        """Adds a driver customer set"""
        
        d,c = range(2)
        
        # Prepare the itinerary for the driver
        stats = cabSet[d].setRoute([cabSet[c],toLocation + (True,)])
            
        self.queue.append(cabSet + (stats,))
        
    def pop(self):
        """Returns customers and drivers to their respective queues"""
        d,c = range(2)
        
        # Continue holding the people who are busy
        self.queue = [i for i in self.queue if i[d].isBusy()]
        
        # Return the people who are not busy
        return [i for i in self.queue if i[d].isBusy() is False]
        
        

class customerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()