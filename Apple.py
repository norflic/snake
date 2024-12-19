import pygame


class Apple(pygame.sprite.Sprite):
    def __init__(self,game):
        super(Apple, self).__init__()
        self.game = game

        self.image = pygame.image.load("C:\\Users\\nils\\Desktop\\cours\\anglais\\snake from brickbreaker\\apple.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))

        self.rect = self.image.get_rect()

        x, y = self.game.get_random_tile()
        self.rect.x = game.convert_tuile_pos(self.game, x)
        self.rect.y = game.convert_tuile_pos(self.game, y)


        