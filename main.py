import pygame
from sprites import *

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

class Game:
    def __init__(self):
        # initialize game
        pygame.init()

        # set up game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Block Blast Buddy")

        # loop game
        self.running = True

        # set up groups
        self.all_sprites = pygame.sprite.Group()

        # load
        self.grid()

    def grid(self):
        # initial pos
        x, y = 0, 0

        # 8x8 block blast grid
        grid_data = [[0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0]]
        
        for row in grid_data:
            for col in row:
                if col == 0:
                    GridBlock((x, y), self.all_sprites)
                x += 46
            x = 0
            y += 46
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    self.running = False
            
            # update
            self.all_sprites.update()

            # draw
            self.screen.fill("white")
            self.all_sprites.draw(self.screen)

            pygame.display.flip()

        # quit game
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()