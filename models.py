import constants

# Models

# User controlled player
class Player:
    def __init__(self, name):
        self.name = name
        self.maxThirst = constants.playerMaxThirst
        self.maxHunger = constants.playerMaxHunger
        self.inventorySize = constants.playerInventorySize
        self.thirst = self.maxThirst
        self.hunger = self.maxHunger
        self.inventory = [None] * self.inventorySize
        print('New player "' + self.name + '" created.')

    def lowerThirst(self):
        self.thirst -= 1
        print('thirst')

    def lowerHunger(self):
        self.hunger -= 1
        print('hunger')

    def addItem(self, item: 'Item', slot=0):
        if (-1 < slot < self.inventorySize) and (self.inventory[slot] == None):
            self.inventory[slot] = item
            print('item added: ' + item.name)

    def removeItem(self, slot):
        if (-1 < slot < self.inventorySize) and (self.inventory[slot] != None):
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
    pass

# All the different areas in the ground segment
class Area:
    pass

# Buying rooms and equipment for the station
class ResearchCenter(Area):
    pass

# For checking the condition of the station
class MissionControl(Area):
    pass

# Ordering food for the missions
class Kitchen(Area):
    pass

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