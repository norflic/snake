from random import randint

import pygame
from pygame.locals import *

from Apple import Apple
from Snake import Snake

SCREEN_WIDTH = 1280//25*25
SCREEN_HEIGHT = 720//25*25
LENGTH_UNIT = 25


def spawn_in_screen():
    case_max_x = round(SCREEN_WIDTH/LENGTH_UNIT)
    case_max_y = round(SCREEN_HEIGHT/LENGTH_UNIT)
    apple_pos_x = randint(0, case_max_x)
    apple_pos_y = randint(0,case_max_y)
    return apple_pos_x, apple_pos_y

def add_apple(apple_list):
    x,y = spawn_in_screen()
    apple = Apple(LENGTH_UNIT, x,y)
    apple_list.append(apple)

# def tick_is_multiple_4(tick_counter):
#     if tick_counter%4 == 0:
#         return True
#     else :
#         return False
def apple_eaten(snake, apple_list, tick_counter, score):
    for apple in apple_list:
        if snake.rect.colliderect(apple.rect):
            infinite_loop = True
            # while infinite_loop:
                # if tick_is_multiple_4(tick_counter):
            add_apple(apple_list)
            snake.add_tail()
            apple_list.remove(apple)
            del apple
            score = (score * 1.1 + 50)
                # infinite_loop = False
    return score


def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    score =0
    tick_counter = 0
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
    snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT, LENGTH_UNIT)
    apple_list = []
    # snake.add_tail()
    for i in range(50):
        add_apple(apple_list)

    first_tail = snake.get_tail(0)

    # apple = Apple(LENGTH_UNIT, 0,0)

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    def display_all():
        for i in range(snake.get_nb_tails()):
            tail = snake.get_tail(i)
            screen.blit(tail.surf, tail.rect)
        for apple in apple_list:
            screen.blit(apple.surf, apple.rect)
        screen.blit(snake.surf, snake.rect)

    def update_all_tails():
        for i in range(snake.get_nb_tails()):
            snake.get_tail(i).update()

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
            score = score*1.001
            # -- listeners and updaters --
            snake.update(pygame.key.get_pressed())
            # if tick_counter % 4 == 0:
            #     print("4 ticks sont passes")
            snake.move()
            update_all_tails()
            score = apple_eaten(snake, apple_list, tick_counter, score)

            # -- display --
            display_all()


            text_score = font.render(f"score : {round(score)}", True, (255, 0, 0))
            text_fps = font.render(f"fps : {clock.get_fps()/2}", True, (255, 0, 0))
            text_snake_debug = font.render(f"snake : {snake}" , True, (255, 0, 0))
            taxt_nb_objects = font.render(f"nb_tails = {snake.get_nb_tails()}  nb_apples = {len(apple_list)}",True, (255, 0, 0))
            screen.blit(text_score, (0, 0))
            screen.blit(text_fps, (0, 35))
            screen.blit(text_snake_debug, (0, 70))
            # screen.blit(taxt_nb_objects, (0, 105))

            pygame.display.flip()

            print(f"snake : {snake}")
            print(f"tail : {snake.get_tail(0)}")

            tick_counter +=1

        clock.tick(5)
    # Done! Time to quit.
    pygame.quit()

if __name__ == '__main__':
    main()