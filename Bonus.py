import pygame

class Bonus(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Bonus, self).__init__()
        self.game = game
        self.effect = self.get_random_effect()

        self.image = pygame.image.load("C:\\Users\\nils\\Desktop\\cours\\anglais\\snake from brickbreaker\\queue.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))

        self.rect = self.image.get_rect()

        x, y = self.game.get_random_tiled_pos()
        self.rect.x = x
        self.rect.y = y

    def convert_pos_tuile(self, pos):
        return (pos * self.game.length_unit)

    def get_random_effect(self):
        return "tp"

    def apply_effect(self):
        match self.effect:
            case "slow":
                self.slow()
            case "fast":
                self.fast()
            case "tp":
                self.tp()
            case "cats":
                self.cats()
            case "rm_tail":
                self.rm_tail()
            case "magnet":
                self.magnet()
            case "ghost":
                self.ghost()
            case "life":
                self.life()
            case _:
                print("cet effet n'existe pas : " + self.effect)

    def slow(self):
        if self.game.tick_multiplier <= 5:
            self.game.tick_multiplier += 1
    def fast(self):
        if self.game.tick_multiplier > 3:
            self.game.tick_multiplier -= 1

    def tp(self):
        pos_margin = self.game.length_unit * 2
        pos_x, pos_y = self.game.get_random_tiled_pos()
        pos_x, pos_y = self.check_tp_pos(pos_margin, pos_x, pos_y)
        self.game.snake.rect.x = pos_x
        self.game.snake.rect.y = pos_y
    # def tp(self):
    #     x, y = self.game.get_random_tile()
    #     pos_x = self.game.convert_tuile_pos(self.game, x)
    #     pos_y = self.game.convert_tuile_pos(self.game, y)
    #     for apple in self.game.apple_list:
    #         if self.game.snake.rect.x != apple.rect.x and self.game.snake.rect.y != apple.rect.y:
    #             self.game.snake.rect.x = pos_x
    #             self.game.snake.rect.y = pos_y
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

    def check_tp_pos(self, margin, pos_x, pos_y):
        # TODO : reparer collision queue
        # if self.check_queue_and_apple(pos_x, pos_y):
        if self.check_x(margin, pos_x):
            if self.check_y(margin, pos_y):
                print(f"posx: {pos_x}, posy: {pos_y}")
                return pos_x, pos_y
            else:
                print(f" le y est pas bon {pos_y}")
        else:
            print(f" le x est pas bon {pos_x}")
        # else:
        #     print(f" coll avec queue")
        pos_x, pos_y = self.game.get_random_tiled_pos()
        return self.check_tp_pos(margin, pos_x, pos_y)

    def check_queue_and_apple(self, pos_x, pos_y):
        for queue in self.game.snake.tail_list:
            if queue.rect.x != pos_x or queue.rect.y != pos_y:
                return True
            else:
                return False

    def check_x(self, pos_margin, pos_x):
        return (pos_x > pos_margin and pos_x < self.game.SCREEN_WIDTH - pos_margin)

    def check_y(self, pos_margin, pos_y):
        return (pos_y > pos_margin and pos_y < self.game.SCREEN_HEIGHT - pos_margin)



