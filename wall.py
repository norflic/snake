import pygame

walls_list = []

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        pygame.sprite.Sprite.__init__(self)
        super(Wall, self).__init__()
        self.game = game

        self.image = pygame.image.load("icons/wall.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
