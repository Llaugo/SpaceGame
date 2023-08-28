import pygame
import constants
import random


# Models


# Container for water
class WaterTank:
    # Determine how much water the tank can hold and what is the initial amount
    def __init__(self, maxAmount=100, startWith=100):
        self.max = maxAmount
        self.amount = min(startWith, maxAmount)
        print('A tank with water: ' + str(self.amount))

    # Fill the tank to full
    def fill(self):
        self.amount = self.max
        print('tank filled')

    # Remove some amount of liquid
    def pour(self, quantity):
        self.amount = max(0, self.amount - quantity)
        print('tank poured, amount left: ' + str(self.amount))


# Non-playable characters that can be interacted with
class NPC:
    pass


# All the different areas in the ground segment
class Area:
    pass


# Buying rooms and equipment for the station
class ResearchCenter(Area):
    def __init__(self):
        self.level = 0
        self.expansions = constants.upgradeExpansions(0)

    # Add some new expansions for the selection
    def upgrade(self):
        self.level += 1
        self.expansions += constants.upgradeExpansions(self.level)


# For checking the condition of the station
class MissionControl(Area):
    pass


# Ordering food for the missions
class Kitchen(Area):
    def __init__(self):
        self.selection = constants.kitchenSelection

    # Each item has 10% chance of changing. Amount of change is determined by gauss' distribution
    def updatePrices(self):
        for i, item in enumerate(self.selection):
            if (random.random() > 0.9):
                newPrice = round(item[2] + random.gauss(0,1))
                self.selection[i] = [item[0], item[1], newPrice]
                print('Food price update: ' + item[0] + ' costs now ' + newPrice)


# All of the bought stuff arrives here
class LoadingBridge(Area):
    def __init__(self):
        self.ready = []
        self.underway = []

    # Move the first order from underway to ready
    def deliver(self):
        if (self.underway != []):
            delivery = self.underway.pop(0)
            self.ready.append(delivery)
            print('order has arrived')

    # Adding a new order for underway
    def newOrder(self, new):
        self.underway.append(new)
        print('new order has been set')

    # Move the next delivered box to being the current
    def unload(self):
        if (self.ready != [] and self.current.isEmpty()):
            delivery = self.ready.pop(0)
            self.current = delivery
            print('order is now accessible')


# For filling water canisters
class WaterTap(Area):
    def __init__(self):
        self.tank = WaterTank(100,100)

    # Place a tank under the tap, does nothing if a tank is already there
    def place(self, newTank: WaterTank):
        if self.tank == None:
            self.tank = newTank
            print('tank placed under the tap')

    # Remove a potential tank and return it
    def pickUp(self):
        if self.tank != None:
            toDel = self.tank
            self.tank = None
            print('tank picked up')
            return toDel

    def fill(self):
        if self.tank != None:
            self.tank.fill()


# Integration and testing facilities is where spacecrafts and utilities are made
class ITFacilities(Area):
    pass


# This is where the rockets are lauched
class Spaceport(Area):
    pass

