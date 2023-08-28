from sys import exit
from models import *
import math

# models imports also pygame, constants and random


# Base class for interactable objects
class Interactable(pygame.sprite.Sprite):

    def draw():
        pass

# User controlled player
class Player(pygame.sprite.Sprite):
    def __init__(self, name, foodbar, waterbar):
        super().__init__()
        pic = pygame.image.load('images/player.png').convert()
        self.image = pygame.transform.rotozoom(pic,0,1.5)
        self.normal = self.image
        self.flipped = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midbottom = (constants.worldWidth/2, constants.distFromGround))
        self.gravity = 0
        self.name = name
        self.thirst = waterbar
        self.hunger = foodbar
        self.money = constants.startingCash

    # All keyboard inputs from players are handled here
    def player_input(self, world, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.image = self.flipped
            if (world.rect.right <= constants.worldWidth or world.rect.left >= 0) and self.rect.left > 5:
                self.rect.x -= constants.playerSpeed
                for wall in walls:
                    if self.rect.colliderect(wall.rect): 
                        self.rect.x += constants.playerSpeed
                        break
        if keys[pygame.K_d]:
            self.image = self.normal
            if (world.rect.right <= constants.worldWidth or world.rect.left >= 0) and self.rect.right < constants.worldWidth-5:
                self.rect.x += constants.playerSpeed
                for wall in walls:
                    if self.rect.colliderect(wall.rect): 
                        self.rect.x -= constants.playerSpeed
                        break
        if keys[pygame.K_SPACE] and self.rect.bottom >= constants.distFromGround:
            self.gravity = -6

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += int(self.gravity)
        if self.rect.bottom >= constants.distFromGround:
            self.rect.bottom = constants.distFromGround

    def update(self, world, walls):
        self.player_input(world, walls)
        self.apply_gravity()
        self.hunger.draw()
        self.thirst.draw()

    def alterHunger(self, amount):
        self.hunger.alterStatus(amount)
    

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('images/world/world.png').convert(),0,1.5)
        self.rect = self.image.get_rect(center = (200,-1070))
        self.objects: list[Interactable] = []

    def addObject(self, object: Interactable): # OBJECTS MUST HAVE A DRAW() FUNCTION
        self.objects.append(object)

    def move(self, movex, movey=0):
        self.rect.x += movex
        self.rect.y += movey
        for obj in self.objects:
            obj.rect.x += movex
            obj.rect.y += movey

    def bg_input(self, player: Player, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.right > constants.worldWidth and player.rect.center[0] >= 0.5*constants.worldWidth:
            self.move(-constants.playerSpeed)
            for wall in walls:
                if player.rect.colliderect(wall.rect): 
                    self.move(constants.playerSpeed)
                    break
        if keys[pygame.K_a] and self.rect.left < 0 and player.rect.center[0] <= 0.5*constants.worldWidth:
            self.move(constants.playerSpeed)
            for wall in walls:
                if player.rect.colliderect(wall.rect): 
                    self.move(-constants.playerSpeed)
                    break

    def update(self, player: Player, walls):
        self.bg_input(player, walls)

# All kinds of stuff that can be carried and held in inventory
class Item:
    def __init__(self, pic, pos, scale, name, amount=1, food=0, drink=0):
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(),0,scale)
        self.rect = self.image.get_rect(center = pos)
        self.pic = pic
        self.scale = scale
        self.name = name
        self.amount = max(min(amount, constants.itemStackSize[name]), 1) # Item amounts must stay inside the limits
        self.food = food # Is the item edible and how much saturation it gives
        self.drink = drink # Is the item drinkable and how much thirst it satisfies

# Can store one item at mouse's position
class HandItem:
    def __init__(self):
        self.item: Item = None
        self.prevClick = 0

    def render(self):
        if self.item:
            pos = pygame.mouse.get_pos()
            self.item.rect = (pos[0]-14,pos[1]-16)
            renderItem(self.item)
            if player.sprite.rect.collidepoint(pos) and (self.item.food or self.item.drink):
                if self.item.food:
                    eat_surf = gamefont_small.render(f'eat {self.item.name} [E]',False,(0,0,0))
                    eat_rect = eat_surf.get_rect(bottomleft = (pos))
                    screen.blit(eat_surf,eat_rect)
                elif self.item.drink:
                    drink_surf = gamefont_small.render(f'drink {self.item.name} [E]',False,(0,0,0))
                    drink_rect = drink_surf.get_rect(bottomleft = (pos))
                    screen.blit(drink_surf,drink_rect)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e] or pygame.mouse.get_pressed()[0]:
                    if not self.prevClick:
                        self.prevClick = 1
                        if self.item.food:
                            player.sprite.hunger.alterStatus(self.item.food)
                        if self.item.drink:
                            player.sprite.thirst.alterStatus(self.item.drink)
                        self.item.amount -= 1
                        if self.item.amount < 1: self.item = None
                else: self.prevClick = 0

class Button(Interactable):
    def __init__(self, pic, picL, pos, scale):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert_alpha(), 0, scale)
        self.imageL = pygame.transform.rotozoom(pygame.image.load(picL).convert_alpha(), 0, scale)
        self.rect = self.image.get_rect(center = pos)
        self.clicked = False
        self.prevclick = 0 # Prevention for holding mouse and moving it over the button. previous event must be "not clicked".

    def draw(self):
        action = False
        touch = False
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            touch = True
            if pygame.mouse.get_pressed()[0] and not self.clicked and not self.prevclick:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.prevclick = 0
            self.clicked = False
        else:
            self.prevclick = 1

        screen.blit(self.image, (self.rect))
        if touch: screen.blit(self.imageL, (self.rect))
        
        return action

# All interactable objects in the game. Same as a button, but instead of mouse it detects collisions with the player(rect)
class Interface(Interactable):
    def __init__(self, pic, picW, x, y, scale):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(), 0, scale)
        self.imageW = pygame.transform.rotozoom(pygame.image.load(picW).convert(), 0, scale)
        self.rect = self.image.get_rect(center = (x,y))

    def draw(self, player: Player):
        action = False
        if self.rect.colliderect(player.rect):
            screen.blit(self.imageW, (self.rect.x-2, self.rect.y-3))
            action = True
        else: screen.blit(self.image, self.rect)
        return action
    
    def update(self,player):
        self.draw(player)

# Borders inside the building
class Wall(Interactable):
    def __init__(self, pic, pos):
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(),0,1.5)
        self.rect = self.image.get_rect(center = pos)
    
    def draw(self, player):
        screen.blit(self.image, self.rect)

# Can hold one item time on it
class InventorySlot(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('images/GUI/slot.png').convert()
        self.imageW = pygame.image.load('images/GUI/slot_white.png').convert()
        self.rect = self.image.get_rect(center = pos)
        self.occupant: Item = None
        self.prevclick = 1 # Prevention for holding mouse and moving it over the button. previous event must be "not clicked".

    def draw(self, pos):
        self.rect.topleft = pos
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.imageW,self.rect)
            #item transfer
            global handItem
            mouse = pygame.mouse.get_pressed()
            if mouse[0] or (mouse[2] and handItem.item and self.occupant):
                if not self.prevclick:
                    self.prevclick = 1
                    if handItem.item and self.occupant and handItem.item.name == self.occupant.name:
                        if mouse[0]:
                            self.occupant.amount += handItem.item.amount
                            handItem.item = None
                        else:
                            self.occupant.amount += 1
                            handItem.item.amount -= 1
                    else:
                        prevHand = handItem.item
                        handItem.item = self.occupant
                        self.occupant = prevHand
            elif mouse[2] and handItem.item:
                if not self.prevclick:
                    self.prevclick = 1
                    self.occupant = Item(handItem.item.pic,handItem.item.rect,handItem.item.scale,handItem.item.name,1,handItem.item.food,handItem.item.drink)
                    handItem.item.amount = handItem.item.amount - 1
            elif mouse[2] and self.occupant:
                if not self.prevclick:
                    self.prevclick = 1
                    half = math.ceil(self.occupant.amount/2)
                    self.occupant.amount -= half
                    handItem.item = Item(self.occupant.pic,self.occupant.rect,self.occupant.scale,self.occupant.name,half,self.occupant.food,self.occupant.drink)
            else: self.prevclick = 0
            if self.occupant and self.occupant.amount < 1: self.occupant = None
            if handItem.item and handItem.item.amount < 1: handItem.item = None
        else: screen.blit(self.image, self.rect)
        if self.occupant: # Item picture and quantity text
            self.occupant.rect = (self.rect.x+4, self.rect.y+3)
            renderItem(self.occupant)


    def addItem(self, item: Item):
        if not item: return True
        elif not self.occupant:
            self.occupant = item
        elif self.occupant.name == item.name:
            self.occupant.amount += item.amount
        else: return False
        return True

    def removeItem(self):
        if self.occupant:
            toDel = self.occupant
            self.occupant = None
            return toDel

# A place to put items into
class Inventory:
    def __init__(self, size):
        self.inventory: list[InventorySlot] = []
        for i in range(size):
            self.inventory.append(InventorySlot((int(constants.worldWidth*(i+7)/(size+13)), constants.worldHeight-40)))

    def draw(self):
        for slot in self.inventory:
            slot.draw((slot.rect.x,slot.rect.y))

# A place to put items into
class Container(Interface):
    def __init__(self, pic, picW, x, y, scale, name, size: int):
        super().__init__(pic,picW,x,y,scale)
        self.open = False
        self.prevclick = 1 # Prevention of flashing inventory while holding w. previous action must be not clicked (=0)
        self.name = name
        self.size = size
        self.spots: list[(InventorySlot,(int, int))] = []
        self.dim = self.factors(size)
        for i in range(int(self.dim[0])):
            for j in range(int(self.dim[1])):
                self.spots.append((InventorySlot((i*40,j*40)), (i*40,j*40)))

    def update(self,player):
        if self.draw(player):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if not self.prevclick:
                    global containers
                    nonOpen = True
                    for box in containers: # Open only if no other container is open
                        if box.open: nonOpen = False
                    if nonOpen or self.open:
                        self.open = self.open ^ True # Toggle state of openness
                        self.prevclick = 1
            else: self.prevclick = 0
            if self.open:
                for i in range(self.size):
                    self.spots[i][0].draw((self.rect.x + self.spots[i][1][0], self.rect.y - 250 + self.spots[i][1][1]))
        else: self.open = False

    # Adds an item to a selected slot
    def addItem(self, item: Item, slot=-1):
        if (-1 < slot < self.size) and self.spots[slot][0].addItem(item):
            return True
        elif slot == -1:
            for i in range(self.size):
                if self.spots[i][0].addItem(item):
                    return True
        else: return False

    # Helper function to get the layout of the container. Returns tuple of dimensions
    def factors(self, n: int):
        dimensions = (1,n)
        if not n % 6:
            if n == 6: dimensions = (2,3)
            else: dimensions = (n/6,6)
        elif not n % 5: dimensions = (n/5,5)
        elif not n % 4:
            if n == 4: dimensions = (2,2)
            else: dimensions = (n/4,4)
        elif not n % 3: dimensions = (n/3,3)
        elif not n % 2: dimensions = (2,n/2)
        return dimensions

# Deletes inserted items
class Garbage(Interface):
    def __init__(self, pic, picW, x, y, scale):
        super().__init__(pic,picW,x,y,scale)
        self.hole = InventorySlot(self.rect.center)

    def update(self, player):
        if self.draw(player):
            self.hole.draw((self.rect.center[0]-18, self.rect.y + 5))
            self.hole.removeItem()

# Keeps track of player statistics
class StatusBar(pygame.sprite.Sprite):
    def __init__(self, pic, piece, name, pos, scale=1):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(),0,scale)
        self.rect = self.image.get_rect(topleft = pos)
        self.piece = pygame.transform.rotozoom(pygame.image.load(piece).convert(),0,scale*1.2)
        self.pRect = self.piece.get_rect(topleft = (pos[0]+38, pos[1]+12))
        self.name = name
        self.percent = 90

    def draw(self):
        for n in range(int(self.percent)):
            screen.blit(self.piece,(self.pRect.x + ((n+1)/100)*270, self.pRect.y))
        screen.blit(self.image, self.rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            status_surf = gamefont_small.render(f'{self.name} is at {self.percent} percent',False,(0,0,0))
            status_rect = score_surf.get_rect(bottomleft = (mouse_pos))
            screen.blit(status_surf,status_rect)

    def alterStatus(self, amount):
        self.percent = max(min((self.percent + amount),100),0)

# Helper function for rendering elevator buttons
def liftButtons(lift: Interface):
    global moveLift
    global floor
    floor1button.rect.topleft = (lift.rect.midtop[0]-50,lift.rect.y-40)
    floor2button.rect.topleft = (lift.rect.midtop[0],lift.rect.y-40)
    floor3button.rect.topleft = (lift.rect.midtop[0]+50,lift.rect.y-40)
    keys = pygame.key.get_pressed()
    if floor1button.draw() or keys[pygame.K_1]:
        if floor == 1: pass
        elif floor == 2: moveLift = -221
        else: moveLift = -440
        floor = 1
    if floor2button.draw() or keys[pygame.K_2]:
        if floor == 1: moveLift = 221
        elif floor == 2: pass
        else: moveLift = -220
        floor = 2
    if floor3button.draw() or keys[pygame.K_3]:
        if floor == 1: moveLift = 440
        elif floor == 2: moveLift = 220
        else: pass
        floor = 3

def renderItem(item: Item):
    screen.blit(item.image, item.rect)
    if item.amount != 1:
        number = gamefont.render(str(item.amount),False,(0,0,0))
        number_rect = number.get_rect(center = (item.rect[0]+22, item.rect[1]+24))
        screen.blit(number, number_rect)

def shop():
    rectangle = pygame.Rect(300, 100, 300, 230)
    pygame.draw.rect(screen, (83,82,87), rectangle)
    for i in range(len(constants.kitchenSelection)):
        currentItem = constants.kitchenSelection[i]
        image = pygame.image.load(constants.itemPictures[currentItem[0]]).convert_alpha()
        img_rect = image.get_rect(topleft = (rectangle.x + 3, rectangle.y + 3 + i*27))
        screen.blit(image, img_rect) # Image
        name_surf = gamefont.render(f'{currentItem[0]}',False,(255,229,120))
        name_rect = name_surf.get_rect(midleft = (img_rect.midright[0] + 5, img_rect.centery))
        screen.blit(name_surf,name_rect) # Name
        name_surf = gamefont.render(f'{currentItem[1]}',False,(255,229,120))
        name_rect = name_surf.get_rect(midleft = (img_rect.midright[0] + 130, img_rect.centery))
        screen.blit(name_surf,name_rect) # Amount
        name_surf = gamefont.render(f'{currentItem[2]}',False,(255,168,98))
        name_rect = name_surf.get_rect(midleft = (img_rect.midright[0] + 200, img_rect.centery))
        screen.blit(name_surf,name_rect) # Cost
        money = pygame.image.load('images/GUI/money_symbol.png').convert_alpha()
        money_rect = money.get_rect(midleft = (img_rect.midright[0] + 220, img_rect.centery))
        screen.blit(money,money_rect) # Money icon




# THE CODE FOR THE GAME STARTS HERE:

pygame.init()
screen = pygame.display.set_mode((constants.worldWidth,constants.worldHeight))
pygame.display.set_caption('Satellite Forge')
pygame.display.set_icon(pygame.image.load('images/player.png'))
clock = pygame.time.Clock()
gamefont = pygame.font.Font('SatelliteForge-Regular.ttf', 25)
gamefont_small = pygame.font.Font('SatelliteForge-Regular.ttf', 23)
gamemode = 'game' # Options: menu, game, pause
floor = 1 # Options: 1, 2, 3
moveLift = 0 # negative down, positive up
handItem = HandItem()

inventory = Inventory(constants.playerInventorySize)
foodbar = StatusBar('images/GUI/foodbar.png','images/GUI/foodbar%.png','Hunger',(10,10),1.5)
waterbar = StatusBar('images/GUI/waterbar.png','images/GUI/waterbar%.png','Thirst',(10,50),1.5)

# Menu screen
menuBack = pygame.image.load('images/menu.jpg').convert()
menurect = menuBack.get_rect(center = (constants.worldWidth/2,constants.worldHeight/2))

playButton = Button('images/GUI/playbutton.png','images/GUI/playbutton_light.png',(480,100),1.5)
menuButton = Button('images/GUI/menubutton.png','images/GUI/menubutton_light.png',(480,200),1.5)
resumeButton = Button('images/GUI/resumebutton.png','images/GUI/resumebutton_light.png',(480,300),1.5)
exitButton = Button('images/GUI/exitbutton.png','images/GUI/exitbutton_light.png',(480,200),1.5)

floor1button = Button('images/GUI/floor1button.png','images/GUI/floor1button_white.png',(0,0),1.5)
floor2button = Button('images/GUI/floor2button.png','images/GUI/floor2button_white.png',(0,0),1.5)
floor3button = Button('images/GUI/floor3button.png','images/GUI/floor3button_white.png',(0,0),1.5)
liftOne = Interface('images/interact/lift1.png','images/interact/lift1_white.png',-236,351,1.5)
liftTwo = Interface('images/interact/lift2.png','images/interact/lift2_white.png',-236,-90,1.5)
liftThree = Interface('images/interact/lift3.png','images/interact/lift3_white.png',-236,-528,1.5)

chest1 = Container('images/interact/chest.png','images/interact/chest_white.png',-1728,430,1.5,'chest',10)
chest2 = Container('images/interact/chest.png','images/interact/chest_white.png',-1072,430,1.5,'chest',10)
chest3 = Container('images/interact/chest.png','images/interact/chest_white.png',200,430,1.5,'chest',10)
barrel1 = Container('images/interact/barrel.png','images/interact/barrel_white.png',-1907,340,1.5,'barrel',8)
barrel2 = Container('images/interact/barrel.png','images/interact/barrel_white.png',-1874,420,1.5,'barrel',8)
barrel3 = Container('images/interact/barrel.png','images/interact/barrel_white.png',-1940,420,1.5,'barrel',8)
crate1 = Container('images/interact/crate.png','images/interact/crate_white.png',-2256,430,1.5,'crate',9)
crate2 = Container('images/interact/crate.png','images/interact/crate_white.png',-1291,311,1.5,'crate',9)
crate3 = Container('images/interact/crate.png','images/interact/crate_white.png',-1540,-10,1.5,'crate',9)
cube1 = Container('images/interact/cube.png','images/interact/cube_white.png',-2134,402,1.5,'cube',16)
cube2 = Container('images/interact/cube.png','images/interact/cube_white.png',-1326,402,1.5,'cube',16)
cube3 = Container('images/interact/cube.png','images/interact/cube_white.png',-1193,402,1.5,'cube',16)
box = Container('images/interact/box.png','images/interact/box_white.png',-1150,322,1.5,'box',4)
containers: list[Container] = [chest1,chest2,chest3,barrel1,barrel2,barrel3,cube1,cube2,cube3,crate1,crate2,crate3,box]

chef = Interface('images/interact/chef.png','images/interact/chef_white.png',-1710,-47,1.5)

garbage = Garbage('images/interact/garbage.png','images/interact/garbage_white.png',629,388,1.5)

onions1 = Item('images/item/onion.png',(100,100),1,'onion',7,2)
onions2 = Item('images/item/onion.png',(100,100),1,'onion',5,2)
bottle = Item('images/item/waterbottle.png',(100,100),1,'water bottle',5,0,5)
melon = Item('images/item/watermelon.png',(100,100),1,'watermelon',1,10,2)
chest3.addItem(melon)
chest3.addItem(onions1)
chest3.addItem(onions2,5)
chest3.addItem(bottle)

wall1 = Wall('images/interact/wall1.png',(-2616,-611))
wall2 = Wall('images/interact/wall2.png',(-2640,-172))
wall3 = Wall('images/interact/wall3.png',(1141,-653))
wall4 = Wall('images/interact/wall4.png',(1070,-174))
walls: list[Wall] = [wall1, wall2, wall3, wall4]

back = Background()
objects = pygame.sprite.Group() # "Background" updates objects' locations correctly and "objects" renders and draws them.
back.addObject(liftOne)
back.addObject(liftTwo)
back.addObject(liftThree)
back.addObject(chef)
back.addObject(garbage)
objects.add(garbage)
for wall in walls:
        back.addObject(wall)
for container in containers:
        back.addObject(container)
        objects.add(container)


background = pygame.sprite.GroupSingle()
background.add(back)

player = pygame.sprite.GroupSingle()
player.add(Player('Steve', foodbar, waterbar))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gamemode == 'game':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gamemode = 'pause'
        elif gamemode == 'pause':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamemode = 'game'
            

    if gamemode == 'menu':
        screen.blit(menuBack,menurect)
        if playButton.draw(): gamemode = 'game'
        if exitButton.draw():
            pygame.quit()
            exit()
   
    elif gamemode == 'game':
        if not moveLift: background.update(player.sprite, walls)
        background.draw(screen)

        if moveLift: # If player is in a lift
            diff = back.rect.x + 1980
            if diff: # First center player to lift
                if diff > 0: back.move(-1)
                elif diff < 0: back.move(1)
            elif moveLift < 0: # Then move player up or down
                moveLift += 1
                back.move(0,-2)
            elif moveLift > 0:
                moveLift -= 1
                back.move(0,2)
        elif liftOne.draw(player.sprite):
            liftButtons(liftOne)
        elif liftTwo.draw(player.sprite):
            liftButtons(liftTwo)
        elif liftThree.draw(player.sprite):
            liftButtons(liftThree)

        if chef.draw(player.sprite):
            shop()
        shop()

        #objects.draw(screen)
        objects.update(player.sprite)

        score_surf = gamefont.render(f'hunger is at {foodbar.percent}',False,(50,50,50))
        score_rect = score_surf.get_rect(center = (750,50))
        screen.blit(score_surf,score_rect)

        if not moveLift or (back.rect.x + 1980): player.draw(screen) # Player vanishes inside the lift
        player.update(background.sprite, walls)

        inventory.draw()
        handItem.render()



    else: # gamemode == 'pause'
        screen.fill((94,129,162))
        if menuButton.draw(): gamemode = 'menu'
        if resumeButton.draw(): gamemode = 'game'

    pygame.display.update()
    clock.tick(60)
