from random import randint

from pygame.locals import *
from pymunk.examples.platformer import height

from Bonus import *
from Apple import *
from Snake import Snake
from wall import walls_list, Wall

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

    def add_snake(self, snake):
        self.snake = snake
    def add_apple(self, nb_apple = 1):
        for i in range(nb_apple):
            apple = Apple(self)
            apple_list.append(apple)
    def add_bonus(self, nb_bonus = 1):
        for i in range(nb_bonus):
            bonus = Bonus(self)
            bonus_list.append(bonus)
    def add_walls(self):
        width = 0
        # horizontal walls
        while width < self.SCREEN_WIDTH:
            wall = Wall(self, width, 0)
            walls_list.append(wall)
            wall = Wall(self, width, self.SCREEN_HEIGHT-self.length_unit)
            walls_list.append(wall)
            width += self.length_unit
        # vertical walls
        height = 0
        while height < self.SCREEN_HEIGHT:
            wall = Wall(self, 0, height)
            walls_list.append(wall)
            wall = Wall(self, self.SCREEN_WIDTH - self.length_unit, height)
            walls_list.append(wall)
            height += self.length_unit

    def tick_is_multiple_4(self):
        if self.tick_counter%4 == 0:
            return True
        else :
            return False

    def score_increase_alive(self):
        self.score = self.score * 1.001

    def get_random_tile(self):
        case_max_x = round(self.SCREEN_WIDTH / self.length_unit)
        case_max_y = round(self.SCREEN_HEIGHT/ self.length_unit)
        x = randint(0, case_max_x-1)
        y = randint(0, case_max_y-1)
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

    def apply_effects(self):
        # magnet
        magnet_index = get_index_of("magnet")
        if effects_dict[magnet_index][1]:
            update_attracted_apples_list()
            move_attracted_apples()
            reduce_effect_time(self, "magnet")

    def resize(self, w, h):
        l = self.length_unit
        self.SCREEN_WIDTH = w // l * l
        self.SCREEN_HEIGHT = w * 9 / 16 // l * l
        screen = pygame.display.set_mode((w // l * l, w * 9 / 16 // l * l), RESIZABLE)
        walls_list.clear()
        self.add_walls()
        return screen


game = Game()

def main():
    screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT), RESIZABLE)
    snake = Snake(game)
    game.add_snake(snake)

    def display_all():
        for i in range(snake.get_nb_tails()):
            tail = snake.get_tail(i)
            screen.blit(tail.image, tail.rect)
        for apple in apple_list:
            screen.blit(apple.image, apple.rect)
        for bonus in bonus_list:
            screen.blit(bonus.image, bonus.rect)
        screen.blit(snake.image, snake.rect)
        for wall in walls_list:
            screen.blit(wall.image, wall.rect)

    # instancie les elements
    game.add_apple(20)
    game.add_bonus(5)
    for i in range(2):
        snake.add_tail()
    game.add_walls()

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

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
                screen = game.resize(event.w, event.h)
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
            apple_eaten(game, snake)
            snake.bonus_eaten()

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