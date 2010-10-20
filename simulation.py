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
    drivers = [] # holds a queue of available drivers
    driving = cab() # holds drivers that are driving people (driver, customer)
    results = [] # holds the results of each completed drive (wait time, trip time, clientRating, driverRating, fare)

    # initialize simulation variables
    random.seed()
    sf = SanFranciscoPointGenerator()
    simulationClock=clock()
    d,c = range(2)
    
    # initialize drivers and customer generator
    [drivers.append(driver(simulationClock,sf.next()))]
    customerGenerator = PoissonGenerator(float(13)/60)
    
    # TEMP
    # p.setRoute([sf.next() + (True,), sf.next() + (False,)])
    # print p.getStats()
    # print p.calculateFare(p.getStats()['billableMiles'])
    # print p.getName()
    
    # simulation loop
    while(simulationClock.getTime() <= 8):
        # 1) process any new customers
        [customers.append(customer(simulationClock,sf.next())) for i in range(customerGenerator.next())]
        
        # 2) process completed rides, add driver back to queue
        for i in driving.pop():
            # put the drivers back
            drivers.append(i[d])
            
            # calculate the results of the customers
            results.append(i[c].getStats())
        
        # 3) assign rides if possible
        [driving.push(i,sf.next()) for i in zip(drivers,customers)]

        # increment the clock
        simulationClock.up()

    # append driver stats now that the simulation is over
    [results.append(i.getStats()) for i in drivers]
    
    # output the results
    print customers
    print drivers
    print driving
    print results

if __name__ == '__main__':
    main()

