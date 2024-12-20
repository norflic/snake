import pygame


class Apple(pygame.sprite.Sprite):
    def __init__(self,game):
        super(Apple, self).__init__()
        self.game = game

        self.image = pygame.image.load("icons/apple.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))

        self.rect = self.image.get_rect()

        x, y = self.game.get_random_tiled_pos()
        self.rect.x = x
        self.rect.y = y


        