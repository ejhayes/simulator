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
        self.queue, self.stats, self.simulationClock, self.initialFare, self.initialDistance, self.farePerMile = [], [], simulationClock, initialFare, initialDistance, farePerMile
        

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
        
        ret['waitTime'] = ret['cabSet'][c]['request'] - self.simulationClock.getTime() + GoogleMaps.toMinutes(driverStats['duration'])
        ret['tripTime'] = GoogleMaps.toMinutes(customerStats['duration'])
        ret['fare'] = self.calculateFare(GoogleMaps.toMiles(customerStats['distance']))
        ret['busyUntil'] = math.ceil(self.simulationClock.getTime() + GoogleMaps.toMinutes(driverStats['duration'] + customerStats['duration']))

        # push the data onto the queue
        self.queue.append(ret)
        
    def pop(self):
        """Returns people who are free"""
        d,c=range(2)
        completedRides = [i for i in self.queue if i['busyUntil'] > self.simulationClock.getTime()]
        self.queue = [i for i in self.queue if i not in completedRides]
        
        # put the stats in
        # wait time, trip time, ratings, fare
        print 'time is %s, %d served, %d riding' % (self.simulationClock.getTime(),len(completedRides),len(self.queue))
        for i in completedRides:
            self.stats.append({
                'tripTime':i['tripTime'],
                'waitTime':i['waitTime'],
                'driverRating':round(random.random()*5),
                'customerRating':round(random.random()*5),
                'fare':i['fare']
            })
        
        # just return the driver information
        return [i['cabSet'][d] for i in completedRides]
    
    def getStats(self):
        """Returns the collected stats"""
        ret = {}
        
        #return dict(zip(self.stats[1].keys(),[sum(j)/len(self.stats) for j in [i.values() for i in self.stats]]))
        ret['tripTime'] = sum([i['tripTime'] for i in self.stats])/len(self.stats)
        ret['waitTime'] = sum([i['waitTime'] for i in self.stats])/len(self.stats)
        ret['driverRating'] = sum([i['driverRating'] for i in self.stats])/len(self.stats)
        ret['customerRating'] = sum([i['customerRating'] for i in self.stats])/len(self.stats)
        ret['fare'] = sum([i['fare'] for i in self.stats])/len(self.stats)
        
        return ret
        

class customerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()