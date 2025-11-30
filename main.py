import pygame

# initialize game
pygame.init()

# set up game window
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Block Blast Buddy")

# loop game
running = True
while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

# quit game
pygame.quit()