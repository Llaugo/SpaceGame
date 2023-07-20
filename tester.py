from models import *

player = Player('Frank')
item1 = Item('potato', 1)
item2 = Item('water bottle')

player.addItem(item1)
print('removed item: ' + player.addItem(item2).name)
print('Player has items:')
for item in player.inventory:
    if item != None:
        print(item.name)
player.removeItem(1)
print('Player has items:')
for item in player.inventory:
    if item != None:
        print(item.name)



player.lowerHunger()
player.lowerHunger()
player.lowerHunger()
print(player.hunger)
print(player.thirst)
player.eat(2)
player.drink()
print(player.hunger)
print(player.thirst)

waterTap = WaterTap()
tank = waterTap.pickUp()
tank.pour(30)
tank.pour(25)
waterTap.place(tank)
waterTap.fill()
print("Now in tank: " + str(tank.amount))
tank.pour(25)
tank.pour(55)
tank.pour(65)
