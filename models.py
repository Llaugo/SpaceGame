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

    # Better hunger by some amount, if not specified set to full
    def eat(self, amount=constants.playerMaxHunger):
        self.hunger = min(constants.playerMaxHunger, self.hunger+amount)
        print('eating, hunger at: (' + self.hunger + '/' + constants.playerMaxHunger + ')')

    # Better thirst by some amount, if not specified set to full
    def drink(self, amount=constants.playerMaxThirst):
        self.thirst = min(constants.playerMaxThirst, self.thirst+amount)
        print('drinking, thirst at: (' + self.hunger + '/' + constants.playerMaxHunger + ')')

    # Pick up an item to inventory
    def addItem(self, item: 'Item', slot=0):
        if (-1 < slot < constants.playerInventorySize) and (self.inventory[slot] == None):
            self.inventory[slot] = item
            print('item added: ' + item.name)

    # Remove an item from inventory
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
        self.amount = max(min(amount, constants.itemStackSize[name]), 1) # Item amounts must stay inside the limits


# Container for water
class WaterTank:
    # Determine how much water the tank can hold and what is the initial amount
    def __init__(self, maxAmount=100, startWith=100):
        self.max = maxAmount
        self.amount = min(startWith, maxAmount)

    # Fill the tank to full
    def fill(self):
        self.amount = self.max

    # Remove some amount of liquid
    def pour(self, quantity):
        self.amount = max(0, self.amount-quantity)


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
        
    def isEmpty(self):
        if not self.spots:
            print("Container is empty")
            return True
        else:
            print("Container not empty")
            return False


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


# big storage area with many containers
class Storage(Area):
    def __init__(self):
        self.crate1 = Container('Crate', 50)
        self.crate2 = Container('Crate', 50)
        self.box1 = Container('Box', 10)
        self.box2 = Container('Box', 10)
        self.box3 = Container('Box', 10)
        self.box4 = Container('Box', 10)
        self.barrel = Container('Barrel', 20)


# All of the bought stuff arrives here
class LoadingBridge(Area):
    def __init__(self):
        self.box = Container('Box', 10)
        self.current = Container('Shipping container', 9)
        self.ready = []
        self.underway = []

    # Move the first order from underway to ready
    def deliver(self):
        if (self.underway != []):
            delivery = self.underway.pop(0)
            self.ready.append(delivery)

    # Adding a new order for underway
    def newOrder(self, new: Container):
        self.underway.append(new)

    # Move the next delivered box to being the current
    def unload(self):
        if (self.ready != [] and self.current.isEmpty()):
            delivery = self.ready.pop(0)
            self.current = delivery


# For filling water canisters
class WaterTap(Area):
    def __init__(self):
        self.tank = WaterTank(100,100)

    # Place a tank under the tap, does nothing if a tank is already there
    def place(self, newTank: WaterTank):
        if self.tank == None:
            self.tank == newTank

    # Remove a potential tank
    def pickUp(self):
        self.tank = None

    def fill(self):
        if self.tank != None:
            self.tank.fill()


# Integration and testing facilities is where spacecrafts and utilities are made
class ITFacilities(Area):
    pass


# This is where the rockets are lauched
class Spaceport(Area):
    pass
