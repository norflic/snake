import pygame


def check_tp_pos(game, margin, pos_x, pos_y):
    if check_queue_and_apple(game, pos_x, pos_y):
        if check_x(game, margin, pos_x):
            if check_y(game, margin, pos_y):
                print(f"posx: {pos_x}, posy: {pos_y}")
                return pos_x, pos_y
            else:
                print(f" le y est pas bon {pos_y}")
        else:
            print(f" le x est pas bon {pos_x}")
    else:
        print(f" coll avec queue")
    pos_x, pos_y = game.get_random_tiled_pos()
    return check_tp_pos(game, margin, pos_x, pos_y)

def check_queue_and_apple(game, pos_x, pos_y):
    for queue in game.snake.tail_list:
        if queue.rect.x != pos_x or queue.rect.y != pos_y:
            return True
        else :
            return False
def check_x(game, pos_margin, pos_x):
    return (pos_x > pos_margin and pos_x < game.SCREEN_WIDTH - pos_margin)
def check_y(game, pos_margin, pos_y):
    return(pos_y > pos_margin and pos_y < game.SCREEN_HEIGHT - pos_margin)

def tp(game):
    pos_margin = game.length_unit * 2
    pos_x, pos_y = game.get_random_tiled_pos()
    pos_x, pos_y = check_tp_pos(game, pos_margin, pos_x, pos_y)
    game.snake.rect.x = pos_x
    game.snake.rect.y = pos_y



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



