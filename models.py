import constants
import random

# Models

# User controlled player
class Player:
    def __init__(self, name):
        self.name = name
        self.thirst = constants.playerMaxThirst
        self.hunger = constants.playerMaxHunger
        self.inventory = [None] * constants.playerInventorySize
        self.money = constants.startingCash
        print('player "' + self.name + '" created.')

    def lowerThirst(self):
        self.thirst -= 1
        print('thirst')

    def lowerHunger(self):
        self.hunger -= 1
        print('hunger')

    def eat(self, amount=constants.playerMaxHunger):
        self.hunger = min(constants.playerMaxHunger, self.hunger+amount)
        print('eating, hunger at: (' + self.hunger + '/' + constants.playerMaxHunger + ')')

    def drink(self, amount=constants.playerMaxThirst):
        self.thirst = min(constants.playerMaxThirst, self.thirst+amount)
        print('drinking, thirst at: (' + self.hunger + '/' + constants.playerMaxHunger + ')')

    def addItem(self, item: 'Item', slot=0):
        if (-1 < slot < constants.playerInventorySize) and (self.inventory[slot] == None):
            self.inventory[slot] = item
            print('item added: ' + item.name)

    def removeItem(self, slot):
        if (-1 < slot < constants.playerInventorySize) and (self.inventory[slot] != None):
            toDel: 'Item' = self.inventory[slot]
            self.inventory[slot] = None
            print('item removed: ' + toDel.name)
            return toDel
    


# Non-playable characters that can be interacted with
class NPC:
    pass

# All kinds of stuff that can be carried and held in inventory
class Item:
    def __init__(self, name, amount=1):
        self.name = name
        self.amount = max(min(amount, constants.itemStackSize[name]), 1)

# A place to put items into
class Container:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.spots = [None] * size

    def addItem(self, item: 'Item', slot=0):
        if (-1 < slot < self.size) and (self.spots[slot] == None):
            self.spots[slot] = item
            print('item ' + item.name + ' added to ' + self.name)

    def removeItem(self, slot):
        if (-1 < slot < self.size) and (self.spots[slot] != None):
            toDel: 'Item' = self.spots[slot]
            self.spots[slot] = None
            print('item ' + toDel.name + ' removed from ' + self.name)
            return toDel

# All the different areas in the ground segment
class Area:
    pass

# Buying rooms and equipment for the station
class ResearchCenter(Area):
    def __init__(self):
        self.level = 0
        self.expansions = constants.upgradeExpansions(0)

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

    def updatePrices(self):
        for i, item in enumerate(self.selection):
            if (random.random() > 0.9):
                newPrice = round(item[2] + random.gauss(0,1))
                self.selection[i] = [item[0], item[1], newPrice]
                print('Food price upgrade: ' + item[0] + ' costs now ' + newPrice)

# big storage area
class Storage(Area):
    pass

# All of the bought stuff arrives here
class LoadingBridge(Area):
    pass

# For filling water canisters
class WaterTap(Area):
    pass

# Integration and testing facilities is where spacecrafts and utilities are made
class ITFacilities(Area):
    pass

# This is where the rockets are lauched
class Spaceport(Area):
    pass