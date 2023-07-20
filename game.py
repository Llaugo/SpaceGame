from sys import exit
from models import *
# models imports also pygame, constants and random



pygame.init()
screen = pygame.display.set_mode((constants.worldWidth,constants.worldHeight))
pygame.display.set_caption('Space Game')
clock = pygame.time.Clock()


background = pygame.sprite.GroupSingle()
background.add(Background())
player = pygame.sprite.GroupSingle()
player.add(Player('Steve'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

   

    background.draw(screen)
    background.update(player.sprite)

    player.draw(screen)
    player.update(background.sprite)


    pygame.display.update()
    clock.tick(60)
