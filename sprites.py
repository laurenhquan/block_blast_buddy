import pygame

BLOCK_SIZE = 45

class GridBlock(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    def select_block(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            selected_pos = pygame.mouse.get_pos()
            if self.rect.left < selected_pos[0] < self.rect.right and self.rect.top < selected_pos[1] < self.rect.bottom:
                self.image.fill('blue')
                # set grid_data pos to 1

        if mouse[2]:
            selected_pos = pygame.mouse.get_pos()
            if self.rect.left < selected_pos[0] < self.rect.right and self.rect.top < selected_pos[1] < self.rect.bottom:
                self.image.fill('grey')
                # set grid_data pos back to 0

    def update(self):
        self.select_block()