import random

import pygame

magnet_attraction_range = 3
effects_dict = [
        ("slow", False, 0),
        ("fast", False, 0),
        ("tp", False, 0),
        ("cat", False, 0),
        ("rm_tail", False, 0),
        ("magnet", False, 0),
        ("ghost", False, 0),
        ("life", False, 0)
        ]
class Bonus(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Bonus, self).__init__()
        self.game = game
        self.effect = None
        self.effect = self.get_random_effect()

        self.image = pygame.image.load("icons/queue.png")
        self.set_image()
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))

        self.rect = self.image.get_rect()

        x, y = self.game.get_random_tiled_pos()
        self.rect.x = x
        self.rect.y = y

    def convert_pos_tuile(self, pos):
        return (pos * self.game.length_unit)

    def set_image(self):
        for i in range(len(effects_dict)):
            # print("set_image" + str(effects_dict[i][0]))
            effet = effects_dict[i][0]
            if self.effect == effet:
                self.image = pygame.image.load("icons/"+effet+".png")
        #     self.rect = self.image.get_rect()
        # if (self.effect == "slow"):
        #     self.image = pygame.image.load("slow.png")
        # if (self.effect == "fast"):
        #     self.image = pygame.image.load("fast.png")
        # if (self.effect == "tp"):
        #     self.image = pygame.image.load("tp.png")
        # if (self.effect == "cat"):
        #     self.image = pygame.image.load("cat.png")
        # # if (self.effect == "rm_tail"):
        # #     self.image = pygame.image.load("rm_tail.png")
        # if (self.effect == "magnet"):
        #     self.image = pygame.image.load("magnet.png")
        # if (self.effect == "ghost"):
        #     self.image = pygame.image.load("ghost.png")
        # if self.effect is None:
        #     self.image = pygame.image.load("queue.png")
    def get_random_effect(self):
        no_effet = random.choice(self.game.fake_dict)
        effet = effects_dict[no_effet][0]
        # print("get_random_effect"+effet)
        return effet
        # print("get_random_effect" +effet2)
        # return "effect"

    def apply_effect(self):
        print("apply_effect" +str(self.effect))
        match self.effect:
            case "slow":
                self.slow()
            case "fast":
                self.fast()
            case "tp":
                self.tp()
            case "cat":
                self.cat()
            case "rm_tail":
                self.rm_tail()
            case "magnet":
                self.magnet()
            case "ghost":
                self.ghost()
            case "life":
                self.life()
            case _:
                print("apply_effect"+str(self))
                print("cet effet n'existe pas : " + str(self.effect))

    def fast(self):
        print("je suis ralenti")
        if self.game.tick_multiplier <= 5:
            self.game.tick_multiplier += 1
    def slow(self):
        print("je suis accelere")
        if self.game.tick_multiplier > 3:
            self.game.tick_multiplier -= 1

    def tp(self):
        pos_margin = self.game.length_unit * 2
        pos_x, pos_y = self.game.get_random_tiled_pos()
        pos_x, pos_y = self.check_tp_pos(pos_margin, pos_x, pos_y)
        self.game.snake.rect.x = pos_x
        self.game.snake.rect.y = pos_y
    def cat(self):
        pass
    def rm_tail(self):
        self.game.snake.remove_tail()
    def magnet(self):
        self.add_time_left("magnet", 1000)
    def ghost(self):
        self.game.snake.add_immunity()
    def life(self):
        self.game.snake.add_life()

    def set_time_left(self, effect_name, time_left):
        effects_dict[get_index_of(effect_name)] = (effect_name, True, time_left)

    def add_time_left(self, effect_name, time_left):
        curr_time = effects_dict[get_index_of(effect_name)][2]
        effects_dict[get_index_of(effect_name)] = (effect_name, True, curr_time+time_left)

    def check_tp_pos(self, margin, pos_x, pos_y):
        if self.check_queue_and_apple(pos_x, pos_y):
            if self.check_x(margin, pos_x):
                if self.check_y(margin, pos_y):
                    print(f"posx: {pos_x}, posy: {pos_y}")
                    return pos_x, pos_y
                else:
                    print(f" le y est pas bon {pos_y}")
            else:
                print(f" le x est pas bon {pos_x}")
        else:
            print(f" coll avec queue")
        pos_x, pos_y = self.game.get_random_tiled_pos()
        return self.check_tp_pos(margin, pos_x, pos_y)

    def check_queue_and_apple(self, pos_x, pos_y):
        for queue in self.game.snake.tail_list:
            if queue.rect.x != pos_x or queue.rect.y != pos_y:
                return True
        return False

    def check_x(self, pos_margin, pos_x):
        return (pos_x > pos_margin and pos_x < self.game.SCREEN_WIDTH - pos_margin)

    def check_y(self, pos_margin, pos_y):
        return (pos_y > pos_margin and pos_y < self.game.SCREEN_HEIGHT - pos_margin)

    def __str__(self):
        return f"self.effect: {self.effect}"
def get_fake_dict(effect_dict):
    fake_dict = []
    for i in range(len(effect_dict)):
        fake_dict.append(i)
    print(fake_dict)
    return fake_dict

def reduce_effect_time(game, effect_name):
    effect_index = get_index_of(effect_name)
    new_time_left = effects_dict[effect_index][2] - game.tick_multiplier
    if new_time_left <= 0:
        effects_dict[effect_index] = (effect_name,False,0)
    else:
        effects_dict[effect_index] = (effect_name, True, new_time_left)

def get_index_of(effect_name):
    for i in range(len(effects_dict)):
        if effect_name == effects_dict[i][0]:
            return i
    print("l'effet "+effect_name+" n'existe pas dans la liste")
    return None