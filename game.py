from sys import exit
from models import *
import math

# models imports also pygame, constants and random



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
        screen.blit(self.image, (self.rect))
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

class InventorySlot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('images/GUI/slot.png').convert()
        self.imageW = pygame.image.load('images/GUI/slot_white.png').convert()
        self.rect = self.image.get_rect(center = (x,y))
        self.occupant: Item = None
        self.prevclick = 1 # Prevention for holding mouse and moving it over the button. previous event must be "not clicked".

    def draw(self, pos):
        self.rect.topleft = pos
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.imageW,self.rect)
            #item transfer
            global handItem
            mouse = pygame.mouse.get_pressed()
            if mouse[0] or (mouse[2] and handItem and self.occupant):
                if not self.prevclick:
                    self.prevclick = 1
                    if handItem and self.occupant and handItem.name == self.occupant.name:
                        if mouse[0]:
                            self.occupant.amount += handItem.amount
                            handItem = None
                        else:
                            self.occupant.amount += 1
                            handItem.amount -= 1
                    else:
                        prevHand = handItem
                        handItem = self.occupant
                        self.occupant = prevHand
            elif mouse[2] and handItem:
                if not self.prevclick:
                    self.prevclick = 1
                    self.occupant = Item(handItem.pic,handItem.rect,handItem.scale,handItem.name)
                    handItem.amount = handItem.amount - 1
            elif mouse[2] and self.occupant:
                if not self.prevclick:
                    self.prevclick = 1
                    half = math.ceil(self.occupant.amount/2)
                    self.occupant.amount -= half
                    handItem = Item(self.occupant.pic,self.occupant.rect,self.occupant.scale,self.occupant.name,half)
            else: self.prevclick = 0
            if self.occupant and self.occupant.amount < 1: self.occupant = None
            if handItem and handItem.amount < 1: handItem = None
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
        if self.occupant != None:
            toDel = self.occupant
            self.occupant = None
            return toDel

class Inventory:
    def __init__(self, size):
        self.inventory: list[InventorySlot] = []
        for i in range(size):
            self.inventory.append(InventorySlot(int(constants.worldWidth*(i+7)/(size+13)), constants.worldHeight-40))

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
                self.spots.append((InventorySlot(i*40,j*40), (i*40,j*40)))

    def update(self,player):
        if self.draw(player):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if not self.prevclick:
                    self.open = self.open ^ True # Toggle state of openness
                    self.prevclick = 1
            else: self.prevclick = 0
            if self.open:
                for i in range(self.size):
                    self.spots[i][0].draw((self.rect.x + self.spots[i][1][0], self.rect.y - 300 + self.spots[i][1][1]))
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
        print(dimensions)
        return dimensions

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


pygame.init()
screen = pygame.display.set_mode((constants.worldWidth,constants.worldHeight))
pygame.display.set_caption('Satellite Forge')
pygame.display.set_icon(pygame.image.load('images/player.png'))
clock = pygame.time.Clock()
gamefont = pygame.font.Font('SatelliteForge-Regular.ttf', 25)
gamemode = 'game' # Options: menu, game, pause
floor = 1 # Options: 1, 2, 3
moveLift = 0 # negative down, positive up
handItem: Item = None # Item currently in hand

inventory = Inventory(8)

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

chest3 = Container('images/interact/chest.png','images/interact/chest_white.png',200,430,1.5,'chest',25)
containers: list[Container] = [chest3]

onions1 = Item('images/item/onion.png',(100,100),1,'onion',7)
onions2 = Item('images/item/onion.png',(100,100),1,'onion',5)
melon = Item('images/item/watermelon.png',(100,100),1,'watermelon')
chest3.addItem(melon)
chest3.addItem(onions1)
chest3.addItem(onions2,2)

wall1 = Wall('images/interact/wall1.png',(-2616,-611))
wall2 = Wall('images/interact/wall2.png',(-2640,-172))
wall3 = Wall('images/interact/wall3.png',(1141,-653))
wall4 = Wall('images/interact/wall4.png',(1070,-174))
walls: list[Wall] = [wall1, wall2, wall3, wall4]
back = Background()
back.addObject(liftOne)
back.addObject(liftTwo)
back.addObject(liftThree)
back.addObject(chest3)
back.addObject(wall1)
back.addObject(wall2)
back.addObject(wall3)
back.addObject(wall4)
background = pygame.sprite.GroupSingle()
background.add(back)
objects = pygame.sprite.Group()
objects.add(chest3)
player = pygame.sprite.GroupSingle()
player.add(Player('Steve'))

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

        objects.update(player.sprite)
        objects.draw(screen)

        score_surf = gamefont.render(f'text',False,(50,50,50))
        score_rect = score_surf.get_rect(center = (150,50))
        screen.blit(score_surf,score_rect)

        if not moveLift or (back.rect.x + 1980): player.draw(screen) # Player vanishes inside the lift
        player.update(background.sprite, walls)

        inventory.draw()

        if handItem:
            handItem.rect = pygame.mouse.get_pos()
            renderItem(handItem)


        

    else: # gamemode == 'pause'
        screen.fill((94,129,162))
        if menuButton.draw(): gamemode = 'menu'
        if resumeButton.draw(): gamemode = 'game'

    pygame.display.update()
    clock.tick(60)
