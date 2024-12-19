import pygame


class Apple(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        super(Apple, self).__init__()
        self.game = game

        self.image = pygame.image.load("C:\\Users\\nils\\Desktop\\cours\\anglais\\snake from brickbreaker\\apple.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))

        self.rect = self.image.get_rect()

        self.rect.x = game.convert_pos_tuile(self.game, x)
        self.rect.y = game.convert_pos_tuile(self.game, y)


        