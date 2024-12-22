import pygame

from Bonus import magnet_attraction_range

apple_list = []

class Apple(pygame.sprite.Sprite):
    def __init__(self,game):
        super(Apple, self).__init__()
        self.game = game
        self.is_attracted = False
        self.speed = self.game.length_unit/self.game.tick_multiplier+2

        self.image = pygame.image.load("icons/apple.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))

        self.rect = self.image.get_rect()

        x, y = self.game.get_random_tiled_pos()
        self.rect.x = x
        self.rect.y = y

    def check_if_attracted(self) -> None:
        snake = self.game.snake
        if abs(abs(self.rect.x)-abs(snake.rect.x)) < self.game.length_unit*magnet_attraction_range:
            if abs(abs(self.rect.y)-abs(snake.rect.y)) < self.game.length_unit*magnet_attraction_range:
                self.is_attracted = True

    def move_towards_snake(self):
        snake = self.game.snake
        if self.rect.y < snake.rect.y:
            self.rect.y += min(self.speed, snake.rect.y - self.rect.y)
        elif self.rect.y > snake.rect.y:
            self.rect.y -= min(self.speed, self.rect.y - snake.rect.y)

        if self.rect.x < snake.rect.x:
            self.rect.x += min(self.speed, snake.rect.x - self.rect.x)
        elif self.rect.x > snake.rect.x:
            self.rect.x -= min(self.speed, self.rect.x - snake.rect.x)


def update_attracted_apples_list(apple_list):
    for apple in apple_list:
        if not apple.is_attracted:
            apple.check_if_attracted()

def move_attracted_apples(apple_list):
    for apple in apple_list:
        if apple.is_attracted:
            apple.move_towards_snake()


        