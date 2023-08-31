


# Models


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


# Integration and testing facilities is where spacecrafts and utilities are made
class ITFacilities(Area):
    pass


# This is where the rockets are lauched
class Spaceport(Area):
    pass

