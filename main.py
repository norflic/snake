from bdb import effective
from random import randint

import pygame
from pygame.locals import *

from Bonus import *
from Apple import *
from Snake import Snake

class Game:
    def __init__(self):
        self.game = self
        self.tick_rate = 5
        self.tick_multiplier = 4
        self.length_unit = 25
        self.SCREEN_WIDTH = 1280//self.length_unit*self.length_unit
        self.SCREEN_HEIGHT = 720//self.length_unit*self.length_unit
        self.score =0
        self.tick_counter = 0
        self.fake_dict = get_fake_dict(effects_dict)
        self.snake =None
        self.bonus_list = []

    def add_snake(self, snake):
        self.snake = snake

    def tick_is_multiple_4(self):
        if self.tick_counter%4 == 0:
            return True
        else :
            return False

    def apple_eaten(self, snake):
        for apple in apple_list:
            if snake.rect.colliderect(apple.rect):
                self.game.add_apple()
                snake.add_tail()
                apple_list.remove(apple)
                del apple
                self.score = (self.score * 1.1 + 50)

    def bonus_eaten(self, snake):
        for bonus in self.game.bonus_list:
            if snake.rect.colliderect(bonus.rect):
                self.game.add_bonus()
                bonus.apply_effect()
                self.bonus_list.remove(bonus)
                del bonus

    def score_increase_alive(self):
        self.score = self.score * 1.001

    def get_random_tile(self):
        case_max_x = round(self.SCREEN_WIDTH / self.length_unit)
        case_max_y = round(self.SCREEN_HEIGHT / self.length_unit)
        x = randint(0, case_max_x)
        y = randint(0, case_max_y)
        return x, y

    def get_random_tiled_pos(self):
        x,y = self.get_random_tile()
        x *= self.length_unit
        y *= self.length_unit
        return x,y

    def get_a_random_tiled_pos(self):
        x,y = self.get_random_tile()
        x *= self.length_unit
        return x

    def add_apple(self):
        apple = Apple(self)
        apple_list.append(apple)

    def add_bonus(self):
        bonus = Bonus(self)
        self.bonus_list.append(bonus)

    def apply_effects(self):
        # magnet
        magnet_index = get_index_of("magnet")
        if effects_dict[magnet_index][1]:
            update_attracted_apples_list(apple_list)
            move_attracted_apples(apple_list)
            reduce_effect_time(self, "magnet")




def main():
    game = Game()
    screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT), RESIZABLE)
    snake = Snake(game)
    game.add_snake(snake)
    # snake.add_tail()
    for i in range(50):
        game.add_apple()
        #
    for i in range(20):
        game.add_bonus()
    for i in range(2):
        snake.add_tail()

    first_tail = snake.get_tail(0)

    # apple = Apple(length_unit, 0,0)

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    def display_all():
        for i in range(snake.get_nb_tails()):
            tail = snake.get_tail(i)
            screen.blit(tail.image, tail.rect)
        for apple in apple_list:
            screen.blit(apple.image, apple.rect)
        for bonus in game.bonus_list:
            screen.blit(bonus.image, bonus.rect)
        screen.blit(snake.image, snake.rect)



    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_a:
                    snake.add_tail()
                if event.key == K_z:
                    snake.get_smallest_tail()
            elif event.type == QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w//25*25, event.w*9/16//25*25), RESIZABLE)
                SCREEN_WIDTH = event.w//25*25
                SCREEN_HEIGHT = event.w*9/16//25*25
                # snake.update_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        # Fill the background with white
        screen.fill((255, 255, 255))
        if snake.is_alive():
            game.score_increase_alive()
            # -- listeners and updaters --
            snake.update(pygame.key.get_pressed())
            # if tick_counter % 4 == 0:
            #     print("4 ticks sont passes")
            game.apply_effects()
            snake.move()
            snake.lose_immunity_by_existing()
            game.apple_eaten(snake)
            game.bonus_eaten(snake)

            # for i in range(snake.get_nb_tails()):
            #     print(str(i)+ " " +str(snake.get_tail(i)))

            # -- display --
            display_all()

            text_score = font.render("score = "+str(round(game.score)), True, (255, 0, 0))
            # text_fps = font.render(f"fps : {clock.get_fps()/2}", True, (255, 0, 0))
            text_snake_debug = font.render(f"snake : {snake}" , True, (255, 0, 0))
            # taxt_nb_objects = font.render(f"nb_tails = {snake.get_nb_tails()}  nb_apples = {len(apple_list)}",True, (255, 0, 0))
            screen.blit(text_score, (0, 0))
            # screen.blit(text_fps, (0, 35))
            screen.blit(text_snake_debug, (0, 70))
            # screen.blit(taxt_nb_objects, (0, 105))

            pygame.display.flip()


            game.tick_counter +=1

        clock.tick(game.tick_rate*game.tick_multiplier)
    # Done! Time to quit.
    pygame.quit()

if __name__ == '__main__':
    main()