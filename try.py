import math
import random
import pygame

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


class rocket(object):
    def __init__(self):
        self.rocket_x = window_x / 2
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
        self.difficulty = 0
        self.speed = 0

    def main_game(self):
        # for specific_ball in balls:
        #     if 0 < specific_ball.x < window_x and 0 < specific_ball.y < window_y:
        #         specific_ball.move()
        #     else:
        #         balls.pop(balls.index(specific_ball))

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
        distance_between_centers =     math.sqrt (  (   ball.x - (rocket.rocket_x + 0.5* rocket.rocket_width)  ) ** 2 + ( ball.y - (rocket.rocket_y + 0.5 * rocket.rocket_height) )** 2  )
        if rocket.rocket_x < ball.x < rocket.rocket_x + rocket.rocket_width:
            if distance_between_centers <= (ball.radius + rocket.rocket_height * 0.5):
                return True

        elif rocket.rocket_y < ball.y < rocket.rocket_y + rocket.rocket_height:
            if distance_between_centers <= (ball.radius + rocket.rocket_width * 0.5):
                return True

        else:
            if distance_between_centers <= (ball.radius + rocket.rocket_width * 0.5 * math.sqrt(2)):
                return True

    return False


def draw_screen():
    window.fill(black)
    rocket.draw()
    # rocket.draw()
    timer = font.render('Time: ' + str(game_state.min) + ':' + str(game_state.sec), 1, (255,255,255))
    window.blit(timer, (300, 20))
    # ball.draw()
    # for i in range(num_of_balls):
    #     balls[i].draw()
    for ball in balls:
        ball.draw()
    pygame.display.update()


# Main Loop
running = True
rocket = rocket()
player = []
balls = []
game_state = game_state()

font = pygame.font.SysFont('comicsans', 20)
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
        rocket.rocket_x = window_x / 2
        rocket.rocket_y = 450
        game_state.state = 'main_game'
    if keys[pygame.K_SPACE] and game_state.state == 'lose':
        game_state.state = 'intro'

    if keys[pygame.K_LEFT] and rocket.rocket_x > 0:
        rocket.rocket_x -= rocket.rocket_vel
    if keys[pygame.K_RIGHT] and rocket.rocket_x < window_x - rocket.rocket_width:
        rocket.rocket_x += rocket.rocket_vel
    if keys[pygame.K_UP] and rocket.rocket_y > 0:
        rocket.rocket_y -= rocket.rocket_vel
    if keys[pygame.K_DOWN] and rocket.rocket_y < window_y - rocket.rocket_height:
        rocket.rocket_y += rocket.rocket_vel

    game_state.state_manager()

pygame.quit()
