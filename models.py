import pygame
import constants
import random

# Models

# User controlled player
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        pic = pygame.image.load('images/steve.png').convert()
        self.image = pygame.transform.rotozoom(pic,0,0.25)
        self.rect = self.image.get_rect(midbottom = (constants.worldWidth/2, constants.distFromGround))
        self.gravity = 0

        self.name = name
        self.thirst = constants.playerMaxThirst
        self.hunger = constants.playerMaxHunger
        self.inventory = [None] * constants.playerInventorySize
        self.money = constants.startingCash
        print('player "' + self.name + '" created.')

    def player_input(self, world):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and (world.rect.right <= constants.worldWidth or world.rect.left >= 0) and self.rect.left > 5:
            self.rect.x -= constants.playerSpeed
        if keys[pygame.K_d] and (world.rect.right <= constants.worldWidth or world.rect.left >= 0) and self.rect.right < constants.worldWidth-5:
            self.rect.x += constants.playerSpeed
        if keys[pygame.K_SPACE] and self.rect.bottom >= constants.distFromGround:
            self.gravity = -10

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += int(self.gravity)
        if self.rect.bottom >= constants.distFromGround:
            self.rect.bottom = constants.distFromGround

    def update(self, world):
        self.player_input(world)
        self.apply_gravity()
    

    def lowerThirst(self):
        self.thirst -= 1
        print('thirst')

    def lowerHunger(self):
        self.hunger -= 1
        print('hunger')

    # Better hunger by some amount, if not specified set to full
    def eat(self, amount=constants.playerMaxHunger):
        self.hunger = min(constants.playerMaxHunger, self.hunger+amount)
        print('eating, hunger at: (' + str(self.hunger) + '/' + str(constants.playerMaxHunger) + ')')

    # Better thirst by some amount, if not specified set to full
    def drink(self, amount=constants.playerMaxThirst):
        self.thirst = min(constants.playerMaxThirst, self.thirst+amount)
        print('drinking, thirst at: (' + str(self.thirst) + '/' + str(constants.playerMaxThirst) + ')')

    # Add an item to inventory. If slot is taken, change items and return the item previously in slot. If empty slot return None
    def addItem(self, item: 'Item', slot=0):
        if (-1 < slot < constants.playerInventorySize):
            if self.inventory[slot] == None:
                self.inventory[slot] = item
                print('item added: ' + item.name)
            else:
                prevItem = self.inventory[slot]
                self.inventory[slot] = item
                print('item added: ' + item.name)
                return prevItem

    # Remove an item from inventory and return that item
    def removeItem(self, slot):
        if (-1 < slot < constants.playerInventorySize) and (self.inventory[slot] != None):
            toDel: 'Item' = self.inventory[slot]
            self.inventory[slot] = None
            print('item removed: ' + toDel.name)
            return toDel


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/astro.jpg').convert()
        self.rect = self.image.get_rect(center = (200,200))

    def bg_input(self, player: Player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.right > constants.worldWidth and player.rect.center[0] >= 0.5*constants.worldWidth:
            self.rect.x -= constants.playerSpeed
        if keys[pygame.K_a] and self.rect.left < 0 and player.rect.center[0] <= 0.5*constants.worldWidth:
            self.rect.x += constants.playerSpeed   

    def update(self, player: Player):
        self.bg_input(player) 


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
        print('A tank with water: ' + str(self.amount))

    # Fill the tank to full
    def fill(self):
        self.amount = self.max
        print('tank filled')

    # Remove some amount of liquid
    def pour(self, quantity):
        self.amount = max(0, self.amount - quantity)
        print('tank poured, amount left: ' + str(self.amount))


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

    # Removes an item from selected slot and returns that item
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
            print('order has arrived')

    # Adding a new order for underway
    def newOrder(self, new: Container):
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

