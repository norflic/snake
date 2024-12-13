import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_s, K_q, K_d

#TODO : faire spawn des queues sur la queue dus serpent
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


    class Tail:
        def __init__(self, snake, game, biggerTail):
            super(Snake.Tail, self).__init__()
            self.snake = snake
            self.game = game
            self.biggerTail = biggerTail
            self.game.length_unit = 25
            self.last_direction = biggerTail.last_direction

            #affichage de la queue
            self.surf = pygame.Surface((self.game.length_unit, self.game.length_unit))
            self.surf.fill(pygame.Color("red"))
            self.rect = self.surf.get_rect()

            x,y = self.get_spawn_position()
            self.rect.x = self.get_spawn_position()[0]
            self.rect.y = self.get_spawn_position()[1]

            self.previous_x = None
            self.previous_y = None

            self.alive = True

        def update(self):
            self.previous_x = self.rect.left
            self.previous_y = self.rect.top

            self.rect.left = self.biggerTail.previous_x
            self.rect.top = self.biggerTail.previous_y

        def add_tail(self):
            new_tail = Snake.Tail(self.snake, self.game,  self)
            return new_tail

        def __str__(self):
            return str(f"bigger_tail = {self.biggerTail} \ttail_self.game.length_unit = {self.game.length_unit} {self.game.length_unit} \tx={self.rect.x} y={self.rect.y}")

        def get_spawn_position(self):
            match self.biggerTail.last_direction:
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
            return self.biggerTail.rect.x+x, self.biggerTail.rect.y+y

    def update(self, pressed_key):
        self.update_dir_pos(pressed_key)
        self.update_coll_queue()
        self.update_coll_walls()

    def update_dir_pos(self, pressed_key):
        if pressed_key[K_UP]:
            self.last_direction = "UP"
        if pressed_key[K_DOWN]:
            self.last_direction = "DOWN"
        if pressed_key[K_LEFT]:
            self.last_direction = "LEFT"
        if pressed_key[K_RIGHT]:
            self.last_direction = "RIGHT"
        if pressed_key[K_z]:
            self.last_direction = "UP"
        if pressed_key[K_s]:
            self.last_direction = "DOWN"
        if pressed_key[K_q]:
            self.last_direction = "LEFT"
        if pressed_key[K_d]:
            self.last_direction = "RIGHT"


    def move(self):
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


    def add_tail(self):
        if len(self.tail_list) != 0:
            new_tail =  self.get_smallest_tail().add_tail()
            self.tail_list.append(new_tail)
        else:
            new_tail = self.Tail(self, self.game, self.get_smallest_tail())
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
        if len(self.tail_list) >=1:
            return self.tail_list[self.get_nb_tails() -1]
        else:
            return self

    def __str__(self):
        return str(f"direction={self.last_direction} nb_tails={len(self.tail_list)} alive={self.alive} x={self.rect.x} y={self.rect.y}")

    def update_coll_queue(self):
        for tail in range(self.get_nb_tails()):
            if self.rect.colliderect(self.get_tail(tail)):
                print("il y  a une collision et c'est pas bien ")
                self.alive = False

    def update_coll_walls(self):
        if (self.rect.x>=self.game.SCREEN_WIDTH-25 and self.last_direction=="RIGHT") or (self.rect.y>=self.game.SCREEN_HEIGHT-25 and self.last_direction=="DOWN"):
            self.alive = False
        if (self.rect.x<0+24 and self.last_direction=="LEFT")or self.rect.y<0+24 and (self.last_direction=="UP"):
            self.alive = False
    def is_alive(self):
        return self.alive
    # def update_screen(self):
    #     self.game.SCREEN_WIDTH = self.game.SCREEN_WIDTH
    #     self.game.SCREEN_HEIGHT = self.game.SCREEN_HEIGHT