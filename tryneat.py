import math
import pickle
import random
import pygame
import os
import neat


# Window
pygame.init()
window_x = 500
window_y = 500
window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Dodge Game')
red = (255, 0, 0)
black = (0, 0, 0)
rocket_image = pygame.image.load('smallreocket.png')
start_image = pygame.image.load('start.png')
gameover_image = pygame.image.load('gameover.png')
num_of_balls = 0
difficulty = 0
speed = 0
num_of_players = 0
gen = 0


class rocket(object):
    def __init__(self, rocket_x):
        self.rocket_x = rocket_x
        self.rocket_y = 450
        self.rocket_width = 15
        self.rocket_height = 25
        self.rocket_vel = 5

    def draw(self):
        window.blit(rocket_image, (self.rocket_x, self.rocket_y))
        pygame.draw.rect(window, black,
                         (round(self.rocket_x), round(self.rocket_y), self.rocket_width, self.rocket_height), 2)

    def move_up(self):
        if self.rocket_y > 0:
            self.rocket_y -= self.rocket_vel

    def move_down(self):
        if self.rocket_y+self.rocket_height < window_y:
            self.rocket_y += self.rocket_vel

    def move_right(self):
        if self.rocket_x > 0:
            self.rocket_x -= self.rocket_vel

    def move_left(self):
        if self.rocket_x+self.rocket_width < window_x:
            self.rocket_x += self.rocket_vel



class ball(object):
    def __init__(self):
        self.x = 250
        self.y = 250
        self.radius = 5
        self.speed = 10
        # self.x_vel = random.randint(-4,5)
        # self.y_vel = random.randint(-1, 1) * math.sqrt(self.speed**2 - self.x_vel**2)
        self.x_vel_vec = random.uniform(-1,1)
        self.y_vel_vec = random.choice([-1,1]) * math.sqrt(1-self.x_vel_vec**2)
        self.x_vel = self.speed * self.x_vel_vec
        self.y_vel = self.speed * self.y_vel_vec

    def draw(self):
        pygame.draw.circle(window, red, (round(self.x), round(self.y)), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


class game_state(object):
    def __init__(self):
        self.state = 'intro'
        self.min = 0
        self.sec = 0
        self.num_of_balls = 0
        # self.num_of_players = num_of_players
        self.difficulty = 0
        self.speed = 0

    def main_game(self):

        for specific_ball in balls:
            specific_ball.move()
            if specific_ball.x <= 0 or specific_ball.x >= 500:
                # specific_ball.x_vel = specific_ball.x_vel * -1
                balls.remove(specific_ball)
            elif specific_ball.y <= 0 or specific_ball.y >= 500:
                # specific_ball.y_vel = specific_ball.y_vel * -1
                balls.remove(specific_ball)


        # if has_collision():
        #     pass
            # game_state.collision()
        self.num_of_balls = 25
        self.difficulty = 10
        self.speed = 10

        # if game_state.sec <= 10 and game_state.min < 1:
        #     self.num_of_balls = 8
        #     self.difficulty = 5
        #     self.speed = 10
        # if game_state.sec > 10 and game_state.min < 1:
        #     self.num_of_balls = 10
        #     self.difficulty = 10
        #     self.speed = 10
        # if game_state.sec > 15 and game_state.min < 1:
        #     self.num_of_balls = 15
        #     self.difficulty = 10
        #     self.speed = 10

        if len(balls) < self.num_of_balls:
            for i in range(self.num_of_balls):
                balls.append(ball())

        # if len(players) < self.num_of_players:
        #     for i in range(self.num_of_players):
        #         if self.num_of_players == 1:
        #             x = 250
        #         elif self.num_of_players ==2:
        #             if i == 0:
        #                 x = 375
        #             if i == 1:
        #                 x = 125
        #
        #         players.append(rocket(x))

        # if len(players) < self.num_of_players:
        #     x = 250
        #     players.append(rocket(x))

        if game_state.sec > 60:
            game_state.min += 1
            game_state.sec = 0
        else:
            game_state.sec += (1 / 20)
        draw_screen()

    def intro(self):
        window.fill(black)
        window.blit(start_image, (165, 220))
        pygame.display.update()

    def lose(self):
        window.blit(gameover_image, (165, 220))
        balls.clear()
        pygame.display.update()

    def state_manager(self):
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'intro':
            self.intro()
        if self.state == 'lose':
            self.lose()

    def collision(self):
        print('hit')
        game_state.state = 'lose'


# def has_collision():
#     for ball in balls:
#         for player in players:
#
#             distance_between_centers = math.sqrt (  (   ball.x - (player.rocket_x + 0.5* player.rocket_width)  ) ** 2 + ( ball.y - (player.rocket_y + 0.5 * player.rocket_height) )** 2  )
#             if player.rocket_x < ball.x < player.rocket_x + player.rocket_width:
#                 if distance_between_centers <= (ball.radius + player.rocket_height * 0.5):
#                     return True
#
#             elif player.rocket_y < ball.y < player.rocket_y + player.rocket_height:
#                 if distance_between_centers <= (ball.radius + player.rocket_width * 0.5):
#                     return True
#
#             else:
#                 if distance_between_centers <= (ball.radius + player.rocket_width * 0.5 * math.sqrt(2)):
#                     return True
#
#     return False

def has_collision(player):
    for ball in balls:

        distance_between_centers = math.sqrt (  (   ball.x - (player.rocket_x + 0.5* player.rocket_width)  ) ** 2 + ( ball.y - (player.rocket_y + 0.5 * player.rocket_height) )** 2  )
        if player.rocket_x < ball.x < player.rocket_x + player.rocket_width:
            if distance_between_centers <= (ball.radius + player.rocket_height * 0.5):
                return True

        elif player.rocket_y < ball.y < player.rocket_y + player.rocket_height:
            if distance_between_centers <= (ball.radius + player.rocket_width * 0.5):
                return True

        else:
            if distance_between_centers <= (ball.radius + player.rocket_width * 0.5 * math.sqrt(2)):
                return True



def draw_screen():
    window.fill(black)
    for player in players:
        player.draw()
    global gen

    timer = font.render('Time: ' + str(game_state.min) + ':' + str(game_state.sec), 1, (255,255,255))
    generation = font.render('Gen: ' + str(gen), 1, (255,255,255))
    window.blit(timer, (300, 20))
    window.blit(generation, (300, 50))

    for ball in balls:
        ball.draw()
    pygame.display.update()



game_state = game_state()
players = []
balls = []
font = pygame.font.SysFont('comicsans', 20)

def main(genomes, config):
# def main():
    global gen
    gen += 1
    game_state.min = 0
    game_state.sec = 0

    nets= []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(rocket(250))
        g.fitness = 0
        ge.append(g)

    # players.append(rocket(250))



    # Main Loop
    running = True
    # rocket = rocket()

    clock = pygame.time.Clock()

    while running:

        for x, player in enumerate(players):
            if has_collision(player):
                # ge[x].fitness -= 2
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
            # elif player.rocket_x <= 0 or player.rocket_x + player.rocket_width >= window_x or player.rocket_y + player.rocket_height <= 0 or player.rocket_y >= window_y:
            #     ge[x].fitness -= 5
            #     players.pop(x)
            #     nets.pop(x)
            #     ge.pop(x)
                # player.rocket_x = 250
                # game_state.state = 'lose'

        clock.tick(20)

        # for x, player in enumerate(players):
        #     ge[x].fitness += 0.01
        #     for ball in balls:
        #         distance = ((player.rocket_x-ball.x)**2 + (player.rocket_y-ball.y)**2)**0.5
        #
        #         # output = nets[x].activate((player.rocket_x, player.rocket_y, ball.x, ball.y))
        #         output = nets[x].activate((player.rocket_x, player.rocket_y, ball.x, ball.y, ball.x_vel_vec, ball.y_vel_vec))
        #
        #         if output[0] > 0.5:
        #             # player.rocket_x -= player.rocket_vel
        #             player.move_up()
        #             ge[x].fitness += 0.1
        #         if output[1] > 0.5:
        #             # player.rocket_x += player.rocket_vel
        #             player.move_down()
        #             ge[x].fitness += 0.1
        #         if output[2] > 0.5:
        #             # player.rocket_y -= player.rocket_vel
        #             player.move_right()
        #             ge[x].fitness += 0.1
        #         if output[3] > 0.5:
        #             # player.rocket_y += player.rocket_vel
        #             player.move_left()
        #             ge[x].fitness += 0.1
        #
        #         if output[0] <= 0.5 and output[1] <= 0.5 and output[2] <= 0.5 and output[3] <= 0.5:
        #             ge[x].fitness -= 2
        game_state.state_manager()

        ball_input = []
        for ball in balls:
            ball_input.append(ball.x)
            ball_input.append(ball.y)
            ball_input.append(ball.x_vel_vec)
            ball_input.append(ball.y_vel_vec)
            # ball_input["ball{0}_x".format(index)] = ball.x
            # ball_input["ball{0}_y".format(index)] = ball.y
            # ball_input["ball{0}_x_vec".format(index)] = ball.x_vel_vec
            # ball_input["ball{0}_y_vec".format(index)] = ball.y_vel_vec

        if len(balls) > 0:
            for x, player in enumerate(players):
                ge[x].fitness += 0.1

                output = nets[x].activate((
                    player.rocket_x, player.rocket_y,
                    ball_input[0], ball_input[1], ball_input[2], ball_input[3],
                    ball_input[4], ball_input[5], ball_input[6], ball_input[7],
                    ball_input[8], ball_input[9], ball_input[10], ball_input[11],
                    ball_input[12], ball_input[13], ball_input[14], ball_input[15],
                    ball_input[16], ball_input[17], ball_input[18], ball_input[19],
                    ball_input[20], ball_input[21], ball_input[22], ball_input[23],
                    ball_input[24], ball_input[25], ball_input[26], ball_input[27],
                    ball_input[28], ball_input[29], ball_input[30], ball_input[31],
                    ball_input[32], ball_input[33], ball_input[34], ball_input[35],
                    ball_input[36], ball_input[37], ball_input[38], ball_input[39],
                    ball_input[40], ball_input[41], ball_input[42], ball_input[43],
                    ball_input[44], ball_input[45], ball_input[46], ball_input[47],
                    ball_input[48], ball_input[49], ball_input[50], ball_input[51],
                    ball_input[52], ball_input[53], ball_input[54], ball_input[55],
                    ball_input[56], ball_input[57], ball_input[58], ball_input[59],
                    ball_input[60], ball_input[61], ball_input[62], ball_input[63],
                    ball_input[64], ball_input[65], ball_input[66], ball_input[67],
                    ball_input[68], ball_input[69], ball_input[70], ball_input[71],
                    ball_input[72], ball_input[73], ball_input[74], ball_input[75],
                    ball_input[76], ball_input[77], ball_input[78], ball_input[79],

                ))

                if output[0] > 0.5:
                    # player.rocket_x -= player.rocket_vel
                    player.move_up()
                    ge[x].fitness += 0.05
                if output[1] > 0.5:
                    # player.rocket_x += player.rocket_vel
                    player.move_down()
                    ge[x].fitness += 0.05
                if output[2] > 0.5:
                    # player.rocket_y -= player.rocket_vel
                    player.move_right()
                    ge[x].fitness += 0.05
                if output[3] > 0.5:
                    # player.rocket_y += player.rocket_vel
                    player.move_left()
                    ge[x].fitness += 0.05

                # if output[0] <= 0.5 and output[1] <= 0.5 and output[2] <= 0.5 and output[3] <= 0.5:
                #     ge[x].fitness -= 2








        if len(players) == 0:
            return
            # running = False
            # break





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game_state.state == 'intro':
            game_state.min = 0
            game_state.sec = 0
            balls.clear()
            # players.clear()
            num_of_players = 1
            #HERE
            game_state.state = 'main_game'
        elif keys[pygame.K_2] and game_state.state == 'intro':
            game_state.min = 0
            game_state.sec = 0
            balls.clear()
            players.clear()
            num_of_players = 2
            # HERE
            game_state.state = 'main_game'

        if keys[pygame.K_SPACE] and game_state.state == 'lose':
            game_state.state = 'intro'

        for player in players:
            if keys[pygame.K_LEFT] and player.rocket_x > 0:
                player.rocket_x -= player.rocket_vel
            if keys[pygame.K_RIGHT] and player.rocket_x < window_x - player.rocket_width:
                player.rocket_x += player.rocket_vel
            if keys[pygame.K_UP] and player.rocket_y > 0:
                player.rocket_y -= player.rocket_vel
            if keys[pygame.K_DOWN] and player.rocket_y < window_y - player.rocket_height:
                player.rocket_y += player.rocket_vel

        if game_state.min > 30:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break
            # if players.index(player) == 0:
            #     if keys[pygame.K_LEFT] and player.rocket_x > 0:
            #         player.rocket_x -= player.rocket_vel
            #     if keys[pygame.K_RIGHT] and player.rocket_x < window_x - player.rocket_width:
            #         player.rocket_x += player.rocket_vel
            #     if keys[pygame.K_UP] and player.rocket_y > 0:
            #         player.rocket_y -= player.rocket_vel
            #     if keys[pygame.K_DOWN] and player.rocket_y < window_y - player.rocket_height:
            #         player.rocket_y += player.rocket_vel
            # if players.index(player) == 1:
            #     if keys[pygame.K_a] and player.rocket_x > 0:
            #         player.rocket_x -= player.rocket_vel
            #     if keys[pygame.K_d] and player.rocket_x < window_x - player.rocket_width:
            #         player.rocket_x += player.rocket_vel
            #     if keys[pygame.K_w] and player.rocket_y > 0:
            #         player.rocket_y -= player.rocket_vel
            #     if keys[pygame.K_s] and player.rocket_y < window_y - player.rocket_height:
            #         player.rocket_y += player.rocket_vel

        # game_state.state_manager()


    # pygame.quit()

# main()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p =neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,200)
    print('\nBest genome:\n{!s}'.format(winner))




if __name__== '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)








