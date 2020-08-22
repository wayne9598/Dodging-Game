import math
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
rocket_image = pygame.image.load('imgs/smallreocket.png')
start_image = pygame.image.load('imgs/start.png')
gameover_image = pygame.image.load('imgs/gameover.png')
num_of_balls = 0
difficulty = 0
speed = 0
num_of_players = 0


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



class ball(object):
    def __init__(self, speed):
        self.x = 250
        self.y = 250
        self.radius = 5
        self.speed = speed
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
        self.num_of_players = 1
        self.difficulty = 0
        self.speed = 0

    def main_game(self):

        for specific_ball in balls:
            specific_ball.move()
            if specific_ball.x <= 0 or specific_ball.x >= 500:
                specific_ball.x_vel = specific_ball.x_vel * -1
            if specific_ball.y <= 0 or specific_ball.y >= 500:
                specific_ball.y_vel = specific_ball.y_vel * -1

        if has_collision():
            game_state.collision()

        if game_state.sec <= 10 and game_state.min < 1:
            self.num_of_balls = 8
            self.difficulty = 5
            self.speed = 10
        if game_state.sec > 10 and game_state.min < 1:
            self.num_of_balls = 10
            self.difficulty = 10
            self.speed = 10
        if game_state.sec > 15 and game_state.min < 1:
            self.num_of_balls = 15
            self.difficulty = 10
            self.speed = 10

        if len(balls) < self.num_of_balls:
            for i in range(self.difficulty):
                balls.append(ball(self.speed))

        if len(players) < self.num_of_players:
            for i in range(self.num_of_players):
                if self.num_of_players == 1:
                    x = 250
                elif self.num_of_players ==2:
                    if i == 0:
                        x = 375
                    if i == 1:
                        x = 125

                players.append(rocket(x))

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


def has_collision():
    for ball in balls:
        for player in players:

            distance_between_centers =     math.sqrt (  (   ball.x - (player.rocket_x + 0.5* player.rocket_width)  ) ** 2 + ( ball.y - (player.rocket_y + 0.5 * player.rocket_height) )** 2  )
            if player.rocket_x < ball.x < player.rocket_x + player.rocket_width:
                if distance_between_centers <= (ball.radius + player.rocket_height * 0.5):
                    return True

            elif player.rocket_y < ball.y < player.rocket_y + player.rocket_height:
                if distance_between_centers <= (ball.radius + player.rocket_width * 0.5):
                    return True

            else:
                if distance_between_centers <= (ball.radius + player.rocket_width * 0.5 * math.sqrt(2)):
                    return True

    return False


def draw_screen():
    window.fill(black)
    for player in players:
        player.draw()

    timer = font.render('Time: ' + str(game_state.min) + ':' + str(game_state.sec), 1, (255,255,255))
    window.blit(timer, (300, 20))

    for ball in balls:
        ball.draw()
    pygame.display.update()


game_state = game_state()
players = []
balls = []
font = pygame.font.SysFont('comicsans', 20)


def main():

    # Main Loop
    running = True
    # rocket = rocket()

    clock = pygame.time.Clock()

    while running:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game_state.state == 'intro':
            game_state.min = 0
            game_state.sec = 0
            balls.clear()
            players.clear()
            num_of_players = 1
            game_state.state = 'main_game'

        elif keys[pygame.K_2] and game_state.state == 'intro':
            game_state.min = 0
            game_state.sec = 0
            balls.clear()
            players.clear()
            num_of_players = 2
            game_state.state = 'main_game'

        if keys[pygame.K_SPACE] and game_state.state == 'lose':
            game_state.state = 'intro'

        for player in players:
            if players.index(player) == 0:
                if keys[pygame.K_LEFT] and player.rocket_x > 0:
                    player.rocket_x -= player.rocket_vel
                if keys[pygame.K_RIGHT] and player.rocket_x < window_x - player.rocket_width:
                    player.rocket_x += player.rocket_vel
                if keys[pygame.K_UP] and player.rocket_y > 0:
                    player.rocket_y -= player.rocket_vel
                if keys[pygame.K_DOWN] and player.rocket_y < window_y - player.rocket_height:
                    player.rocket_y += player.rocket_vel
            if players.index(player) == 1:
                if keys[pygame.K_a] and player.rocket_x > 0:
                    player.rocket_x -= player.rocket_vel
                if keys[pygame.K_d] and player.rocket_x < window_x - player.rocket_width:
                    player.rocket_x += player.rocket_vel
                if keys[pygame.K_w] and player.rocket_y > 0:
                    player.rocket_y -= player.rocket_vel
                if keys[pygame.K_s] and player.rocket_y < window_y - player.rocket_height:
                    player.rocket_y += player.rocket_vel

        game_state.state_manager()


    pygame.quit()

main()
