#!/usr/bin/env python
# encoding: utf-8
"""
simulation.py
Purpose: Performs a simulation of people requesting a cab in San Francisco

Assumptions:
- Drivers begin the simulation at random locations inside the city
- Client requests come from random location inside the city, and clients are to be dropped off at random locations
- Defining the city with a rectangular boundary, as opposed to the real-world shape of the peninsula, is acceptable
- Over the course of the simulated hour, requests come in at random times, or for bonus points, following a Poisson distribution

Calculates and displays the following for each trip: 
- Wait time (time from request to pickup per Google Maps API)
- Trip time (time from pickup to dropoff per Google Maps API)
- Client rating (randomly assigned)
- Driver rating (randomly assigned)
- Fare (use standard taxi rates)

Additional requirements:
- Calculate and display averages (wait time, trip time, client rating, driver rating, fare) for all simulated trips
- Allow a user to select a trip and see it displayed on a Google Map
- Bonus points if your code has good test coverage
"""

import sys
import os
import math
import random
from person import *
from map import GoogleMaps

class clock:
    """The simulation clock"""

    def __init__(self, startTime=0):
        self.time = startTime
        
    def up(self, quantity=1):
        """Increment the clock"""
        self.time += quantity
        
    def getTime(self):
        return self.time

def PoissonGenerator(l):
    """Returns a random poisson distributed number for a given lambda value"""
    l = math.exp(-l)
    k = 0
    p = 1.0

    while(True):
        k += 1
        p *= random.random()

        if(p <= l):
            yield k - 1
            k = 0
            p = 1.0

def SanFranciscoPointGenerator():
    """Generates random latitude/longitude point sets of San Francisco"""
    
    latitudeEast = -122.527
    latitudeWest = -122.3482
    longitudeNorth = 37.812
    longitudeSouth = 37.7034
    
    while(True):
        yield (((longitudeNorth - longitudeSouth) * random.uniform(0,1)) + longitudeSouth, \
        ((latitudeEast - latitudeWest) * random.uniform(0,1)) + latitudeWest)


def main():
    """Runs the simulation"""

    # setup our various waiting queues
    customers = [] # holds a queue of waiting customers

    # initialize simulation variables
    random.seed()
    sf = SanFranciscoPointGenerator()
    simulationClock=clock()
    d,c = range(2)
    
    # initialize drivers and customer generator
    driving = cab(simulationClock) # holds drivers that are driving people (driver, customer)
    
    drivers = [{'start':sf.next()} for i in range(5)]
    customerGenerator = PoissonGenerator(float(50)/60)
    
    # simulation loop
    while(simulationClock.getTime() <= 60):
        # 1) process any new customers 
        [customers.append({'request':simulationClock.getTime(),'start':sf.next(),'end':sf.next()}) for i in range(customerGenerator.next())]
        
        # 2) process completed rides, add driver back to queue
        [drivers.append(i) for i in driving.pop()]
        
        # 3) assign rides if possible'
        for i in drivers:
            if len(customers) > 0:
                # assign the driver to a customer
                driving.push((drivers.pop(),customers.pop()))
            else:
                # if there are no customers, break out!
                break
        

        # 4) increment the clock
        simulationClock.up()
    
    # output the results
    print 'Customers %d' % len(customers)
    print 'Drivers %d' % len(drivers)
    print driving.getStats()
    
if __name__ == '__main__':
    main()

