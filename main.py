import math
import pygame as py

py.init()

clock = py.time.Clock()

FrameHeight = 800
FrameWidth = 600

# tworzenie okna gry
py.display.set_caption("Endless Scrolling in pygame")
screen = py.display.set_mode((FrameWidth,
                              FrameHeight))

# tlo
bg = py.image.load("textures/tlogry.png").convert()


scroll = 0

# ile obrazkow ma byc w bufforze
tiles = math.ceil(FrameHeight / bg.get_height()) + 1

# glowna petla
while 1:
    # predkosc tla
    clock.tick(33)

    
    i = 0
    while (i < tiles):
        screen.blit(bg, (0
                         , bg.get_height() * i +scroll))
        i += 1
    
    scroll -= 6

    # resetowanie scrolla
    if abs(scroll) > bg.get_height():
        scroll = 0
        
        
  # zamykanie scrola
    for event in py.event.get():
        if event.type == py.QUIT:
            quit()

    py.display.update()

py.quit()
