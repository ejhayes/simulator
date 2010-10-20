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

class cab:
    """
    The cab class
    """
    
    def __init__(self,simulationClock, initialFare=2.85, initialDistance=0.2, farePerMile=2.25):
        self.queue, self.stats, self.simulationClock, self.initialFare, self.initialDistance, self.farPerMile = [], [], simulationClock, initialFare, initialDistance, farePerMile
        

    def calculateFare(self, distance):
        """Calculate the fare of a ride"""
        if distance > self.initialDistance:
            rate = 0.0
            distance -= self.initialDistance
            rate += self.initialFare
            rate += distance * self.farePerMile
            return rate
        else:
            return self.initialFare

    def push(self,cabSet):
        """Configures a ride"""
        
        d,c = range(2)

        # our return dictionary
        ret = {}

        # add our ride situation
        ret['cabSet'] = cabSet

        # Get directions from driver to customer (not billed)
        driverStats = GoogleMaps.getDirections(cabSet[d]['start'],cabSet[c]['start'])

        # Get directions for the route (billed)
        customerStats = GoogleMaps.getDirections(cabSet[c]['start'],cabSet[c]['end'])
        
        ret['waitTime'] = self.simulationClock.getTime() - ret['cabSet'][c]['request']
        ret['tripTime'] = GoogleMaps.toMinutes(customerStats['duration'])
        ret['fare'] = calculateFare(GoogleMaps.toMiles(customerStats['distance']))
        ret['busyUntil'] = math.ceil(self.simulationClock.getTime() + GoogleMaps.toMinutes(ret['driverStats']['duration'] + ret['customerStats']['duration']))
        
        # push the data onto the queue
        self.queue.push(ret)
        
    def pop(self):
        """Returns people who are free"""
        completedRides = [i for i in driving if i['busyUntil'] <= simulationClock.getTime()]
        self.queue = [i for i in driving if i not in completedRides]
        
        # put the stats in
        # wait time, trip time, ratings, fare
        for i in completedRides:
            self.stats.append({
                'tripTime':i['tripTime'],
                'waitTime':i['waitTime'],
                'driverRating':3,
                'customerRating':4,
                'fare':i['fare']
            })
        
        # just return the driver information
        return [i['cabSet'][d] for i in completedRides]
    
    def getStats(self):
        """Returns the collected stats"""
        return self.stats
        
        

class customerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()