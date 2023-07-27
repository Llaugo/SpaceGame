from sys import exit
from models import *

# models imports also pygame, constants and random


pygame.init()
screen = pygame.display.set_mode((constants.worldWidth,constants.worldHeight))
pygame.display.set_caption('Space Game')
pygame.display.set_icon(pygame.image.load('images/astro.jpg'))
clock = pygame.time.Clock()
gamemode = 'menu' # Options: menu, game, pause


class Button(pygame.sprite.Sprite):
    def __init__(self, pic, x, y, scale):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(), 0, scale)
        self.rect = self.image.get_rect(center = (x,y))
        self.clicked = False
        self.prevclick = 0 # Prevention for holding mouse and moving it over the button. previous event must be "not clicked".

    def draw(self):
        action = False
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            # change color
            if pygame.mouse.get_pressed()[0] and not self.clicked and not self.prevclick:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.prevclick = 0
            self.clicked = False
        else:
            self.prevclick = 1

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# All interactable objects in the game
class Interface(pygame.sprite.Sprite):
    def __init__(self, pic, picW, x, y, scale):
        self.open = False
        self.image = pygame.transform.rotozoom(pygame.image.load(pic).convert(), 0, scale)
        self.imageW = pygame.transform.rotozoom(pygame.image.load(picW).convert(), 0, scale)
        self.rect = self.image.get_rect(center = (x,y))

    def draw(self, player: Player):
        if self.rect.colliderect(player.rect):
            screen.blit(self.imageW, (self.rect.x, self.rect.y))
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Menu screen
menuBack = pygame.image.load('images/menu.jpg').convert()
menurect = menuBack.get_rect(center = (constants.worldWidth/2,constants.worldHeight/2))


playButton = Button('images/play.png',480,100,0.2)
menuButton = Button('images/menutxt.png',480,200,0.3)

machine = Interface('images/machine.png','images/machine_white.png',-200,430,0.4)

back = Background()
back.addObject(machine)
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
   
    elif gamemode == 'game':
        background.draw(screen)
        background.update(player.sprite)

        player.draw(screen)
        player.update(background.sprite)


    else: # gamemode == 'pause'
        screen.fill((94,129,162))
        if menuButton.draw(): gamemode = 'menu'

    pygame.display.update()
    clock.tick(60)
