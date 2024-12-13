import pygame


class Apple(pygame.sprite.Sprite):
    def __init__(self,length_unit, x, y):
        super(Apple, self).__init__()
        self.length_unit = length_unit
        self.size = length_unit
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(pygame.Color("red"))

        self.rect = self.surf.get_rect()

        # self.rect.x = self.convert_pos_tuile(x)
        # self.rect.y = self.convert_pos_tuile(y)
        self.rect.x = self.convert_pos_tuile(x)
        self.rect.y = self.convert_pos_tuile(y)

    def convert_pos_tuile(self, pos):
        return (pos*self.length_unit)
        