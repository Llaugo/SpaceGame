from sys import exit
from models import *

# models imports also pygame, constants and random


pygame.init()
screen = pygame.display.set_mode((constants.worldWidth,constants.worldHeight))
pygame.display.set_caption('Satellite Forge')
pygame.display.set_icon(pygame.image.load('images/player.png'))
clock = pygame.time.Clock()
gamefont = pygame.font.Font('SatelliteForge-Regular.ttf', 50)
gamemode = 'game' # Options: menu, game, pause
floor = 1 # Options: 1, 2, 3
moveLift = 0 # negative down, positive up



class Button(Interactable):
    def __init__(self, pic, picL, x, y, scale):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert_alpha(), 0, scale)
        self.imageL = pygame.transform.rotozoom(pygame.image.load(picL).convert_alpha(), 0, scale)
        self.rect = self.image.get_rect(center = (x,y))
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
        self.open = False
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(), 0, scale)
        self.imageW = pygame.transform.rotozoom(pygame.image.load(picW).convert(), 0, scale)
        self.rect = self.image.get_rect(center = (x,y))

    def draw(self, player: Player):
        action = False
        if self.rect.colliderect(player.rect):
            screen.blit(self.imageW, (self.rect.x-1, self.rect.y-1))
            action = True
        screen.blit(self.image, (self.rect))
        return action

# Borders inside the building
class Wall(Interactable):
    def __init__(self, pic, x, y):
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(),0,1.5)
        self.rect = self.image.get_rect(center = (x,y))
    
    def draw(self, player):
        screen.blit(self.image, self.rect)

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


# Menu screen
menuBack = pygame.image.load('images/menu.jpg').convert()
menurect = menuBack.get_rect(center = (constants.worldWidth/2,constants.worldHeight/2))


playButton = Button('images/GUI/playbutton.png','images/GUI/playbutton_light.png',480,100,1.5)
menuButton = Button('images/GUI/menubutton.png','images/GUI/menubutton_light.png',480,200,1.5)
resumeButton = Button('images/GUI/resumebutton.png','images/GUI/resumebutton_light.png',480,300,1.5)
exitButton = Button('images/GUI/exitbutton.png','images/GUI/exitbutton_light.png',480,200,1.5)

floor1button = Button('images/GUI/floor1button.png','images/GUI/floor1button_white.png',0,0,1.5)
floor2button = Button('images/GUI/floor2button.png','images/GUI/floor2button_white.png',0,0,1.5)
floor3button = Button('images/GUI/floor3button.png','images/GUI/floor3button_white.png',0,0,1.5)
liftOne = Interface('images/interact/lift1.png','images/interact/lift1_white.png',-236,351,1.5)
liftTwo = Interface('images/interact/lift2.png','images/interact/lift2_white.png',-236,-90,1.5)
liftThree = Interface('images/interact/lift3.png','images/interact/lift3_white.png',-236,-528,1.5)

inventory = pygame.image.load('images/GUI/inventory.png').convert_alpha()
inventory_rect = inventory.get_rect(center = (constants.worldWidth/2, constants.worldHeight-50))

wall4 = Wall('images/interact/wall4.png',1070,-174)
walls: list[Wall] = [wall4]
back = Background()
back.addObject(liftOne)
back.addObject(liftTwo)
back.addObject(liftThree)
back.addObject(wall4)
background = pygame.sprite.GroupSingle()
background.add(back)
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
        background.draw(screen)
        if not moveLift: background.update(player.sprite, walls)

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

        score_surf = gamefont.render(f'movelift {moveLift}',False,(50,50,50))
        score_rect = score_surf.get_rect(center = (150,50))
        screen.blit(score_surf,score_rect)

        if not moveLift or (back.rect.x + 1980): player.draw(screen) # Player vanishes inside the lift
        player.update(background.sprite, walls)

        screen.blit(inventory,inventory_rect)
        

    else: # gamemode == 'pause'
        screen.fill((94,129,162))
        if menuButton.draw(): gamemode = 'menu'
        if resumeButton.draw(): gamemode = 'game'

    pygame.display.update()
    clock.tick(60)
