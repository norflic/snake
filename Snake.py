import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_s, K_q, K_d

class Snake(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Snake, self).__init__()
        #surface
        self.game = game
        self.surf = pygame.Surface((self.game.length_unit, self.game.length_unit))
        self.surf.fill(pygame.Color("black"))
        self.rect = self.surf.get_rect()

        self.last_direction = "RIGHT"
        self.tail_list = []
        # self.tail_list.append(self)

        #deplacement
        self.rect.x = (self.game.SCREEN_WIDTH / 2)//25*25 - self.surf.get_width() / 2//25*25
        self.rect.y = (self.game.SCREEN_HEIGHT / 2)//25*25 - self.surf.get_height() / 2//25*25
        self.previous_x = None
        self.previous_y = None

        self.life = 5
        self.immunity = 0
        self.alive = True


    class Tail:
        def __init__(self, snake, game, bigger_tail):
            super(Snake.Tail, self).__init__()
            self.snake = snake
            self.game = game
            self.bigger_tail = bigger_tail
            self.game.length_unit = 25
            self.last_direction = bigger_tail.last_direction

            self.image = pygame.image.load("icons/queue.png")
            self.image = self.image.convert()
            self.image = pygame.transform.scale(self.image, (self.game.length_unit, self.game.length_unit))


            #affichage de la queue
            # self.surf = pygame.Surface((self.game.length_unit, self.game.length_unit))
            # self.surf.fill(pygame.Color("red"))
            self.rect = self.image.get_rect()

            x,y = self.get_spawn_position()
            self.rect.x = self.get_spawn_position()[0]
            self.rect.y = self.get_spawn_position()[1]

            self.previous_x = None
            self.previous_y = None

        def update(self):
            self.previous_x = self.rect.left
            self.previous_y = self.rect.top

            self.rect.left = self.bigger_tail.previous_x
            self.rect.top = self.bigger_tail.previous_y

        def add_tail(self):
            new_tail = Snake.Tail(self.snake, self.game,  self)
            return new_tail

        def __str__(self):
            return str(f"bigger_tail = {self.bigger_tail} \ttail_self.game.length_unit = {self.game.length_unit} {self.game.length_unit} \tx={self.rect.x} y={self.rect.y}")

        def get_spawn_position(self):
            match self.bigger_tail.last_direction:
                case "UP":
                    x = 0
                    y =-self.game.length_unit
                case "DOWN":
                    x = 0
                    y = self.game.length_unit
                case "LEFT":
                    x = +self.game.length_unit
                    y = 0
                case "RIGHT":
                    x = -self.game.length_unit
                    y = 0
            return self.bigger_tail.rect.x+x, self.bigger_tail.rect.y+y

    def update(self, pressed_key):
        self.update_dir_pos(pressed_key)
        self.update_coll_queue()
        self.update_coll_walls()

    def update_dir_pos(self, pressed_key):
        if pressed_key[K_UP] or pressed_key[K_z]:
            self.last_direction = "UP"
        if pressed_key[K_DOWN] or pressed_key[K_s]:
            self.last_direction = "DOWN"
        if pressed_key[K_LEFT] or pressed_key[K_q]:
            self.last_direction = "LEFT"
        if pressed_key[K_RIGHT] or pressed_key[K_d]:
            self.last_direction = "RIGHT"

    def move(self):
        if self.game.tick_is_multiple_4():
            self.previous_x = self.rect.left
            self.previous_y = self.rect.top
            match self.last_direction:
                case "UP":
                        self.rect.move_ip(0, -self.game.length_unit)
                case "DOWN":
                        self.rect.move_ip(0, self.game.length_unit)
                case "LEFT":
                        self.rect.move_ip(-self.game.length_unit, 0)
                case "RIGHT":
                        self.rect.move_ip(self.game.length_unit, 0)

            self.update_all_tails()

    def update_all_tails(self):
        for i in range(self.get_nb_tails()):
            self.get_tail(i).update()


    def add_tail(self):
        smallest_tail = self.get_smallest_tail()
        if smallest_tail is None:
            new_tail = Snake.Tail(self, self.game,  self)
        else:
            new_tail = smallest_tail.add_tail()
        self.tail_list.append(new_tail)

    def get_tails_list(self):
        return self.tail_list

    def get_tail(self, index):
        if index >= len(self.tail_list):
            return None
        return self.tail_list[index]

    def get_nb_tails(self):
        return len(self.tail_list)

    def get_smallest_tail(self):
        if len(self.tail_list) >0:
            return self.tail_list[len(self.tail_list)-1]
        else:
            return None

    def remove_tail(self):
        if len(self.tail_list)>0:
            self.tail_list.pop()

    def __str__(self):
        return str(f"direction={self.last_direction} nb_tails={len(self.tail_list)} alive={self.alive} immunity = {self.immunity} x={self.rect.x} y={self.rect.y}")

    def update_coll_queue(self):
        for tail in range(self.get_nb_tails()):
            if self.rect.colliderect(self.get_tail(tail)):
                print("il y  a une collision et c'est pas bien ")
                self.loose_hp()

    def update_coll_walls(self):
        if (self.rect.x>=self.game.SCREEN_WIDTH-25 and self.last_direction=="RIGHT") or (self.rect.y>=self.game.SCREEN_HEIGHT-25 and self.last_direction=="DOWN"):
            self.alive = False
        if (self.rect.x<0+24 and self.last_direction=="LEFT")or self.rect.y<0+24 and (self.last_direction=="UP"):
            self.alive = False

    def loose_hp(self):
        if (self.immunity <= 0):
            self.life = self.life - 1
            self.immunity = self.immunity + self.game.tick_multiplier
        if self.life <= 0:
            self.alive = False
            return self.alive

    def lose_immunity_by_existing(self):
        if (self.immunity > 0):
            self.immunity -=1

    def gain_immunity(self):
        self.immunity += self.game.tick_multiplier*5

    def is_alive(self):
        return self.alive