import pygame


def tp(game):
    margin = game.length_unit * 3
    x, y = game.get_random_tile()
    pos_x = game.convert_tuile_pos(game, x)
    pos_y = game.convert_tuile_pos(game, y)
    snake = game.snake
    for apple in game.apple_list:
        if snake.rect.x != apple.rect.x and snake.rect.y != apple.rect.y and pos_x > margin  and  pos_y > margin and pos_x < game.SCREEN_WIDTH - margin and pos_y < game.SCREEN_HEIGHT - margin:
            snake.rect.x = pos_x
            snake.rect.y = pos_y
        # else :
        #     tp(game)

class Bonus(pygame.sprite.Sprite):
    def __init__(self, game, length_unit, x, y, effect):
        super(Bonus, self).__init__()
        self.game = game
        self.effect = effect

        self.image = pygame.image.load("C:\\Users\\nils\\Desktop\\cours\\anglais\\snake from brickbreaker\\queue.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (length_unit, length_unit))

        self.rect = self.image.get_rect()

        self.rect.x = self.convert_pos_tuile(x)
        self.rect.y = self.convert_pos_tuile(y)

    def convert_pos_tuile(self, pos):
        return (pos * self.game.length_unit)

    def apply_effect(self):
        match self.effect:
            case "slow":
                self.slow(self)
            case "fast":
                self.fast(self)
            case "tp":
                self.tp(self)
            case "cats":
                self.cats(self)
            case "rm_tail":
                self.rm_tail(self)
            case "magnet":
                self.magnet(self)
            case "ghost":
                self.ghost(self)
            case "life":
                self.life(self)
        while True:
            print("cet effet n'existe pas : " + self.effect)

    def slow(self):
        if self.game.tick_multiplier <= 5:
            self.game.tick_multiplier += 1
    def fast(self):
        if self.game.tick_multiplier > 3:
            self.game.tick_multiplier -= 1
    def tp(self):
        x, y = self.game.get_random_tile()
        pos_x = self.game.convert_tuile_pos(self.game, x)
        pos_y = self.game.convert_tuile_pos(self.game, y)
        for apple in self.game.apple_list:
            if self.game.snake.rect.x != apple.rect.x and self.game.snake.rect.y != apple.rect.y:
                self.game.snake.rect.x = pos_x
                self.game.snake.rect.y = pos_y
    def cats(self):
        pass
    def rm_tail(self):
        pass
    def magnet(self):
        pass
    def ghost(self):
        pass
    def life(self):
        pass



