import pygame
import random
import math
import time
from snakeobj import Snake

# initalizing pygame
pygame.init()

# set up window and
W, H = 300, 300
Actual_W, Actual_H = W, H  # W + 100, H + 100
WIND = pygame.display.set_mode((Actual_W, Actual_H))
pygame.display.set_caption('Snake')

# set up game var
running = True
FPS = 60
timer = 0
clock = pygame.time.Clock()
black = (0, 0, 0)

# grid set up
GRID_W, GRID_H = 20, 20
num_rows = num_cols = W//GRID_W
white = (255, 255, 255)

# Snake var set up
W_SNAKE = H_SNAKE = 20
x = math.ceil(num_rows/2.0) * GRID_W
y = math.ceil(num_cols/2.0) * GRID_H
speed = (-W_SNAKE, 0) #not needed
border = 3
snake_color = green = (0, 255, 0)
snakeobj = Snake(x, y, W_SNAKE, H_SNAKE, speed)
score = 0

# Food car set up
W_FOOD = H_FOOD = 20
x_f = random.choice(range(0, W - W_FOOD, GRID_W))
y_f = random.choice(range(0, H - H_FOOD, GRID_H))
food_color = red = (255, 0, 0)


def draw():
    global white, x_f, y_f, W_FOOD, H_FOOD, score

    # Clear screen
    WIND.fill(black)

    # Draw Food
    pygame.draw.rect(WIND, food_color, (x_f, y_f, W_FOOD, H_FOOD))

    # Draw Snake parts
    rects = snakeobj.draw()
    for rect in rects:
        pygame.draw.rect(WIND, snake_color, rect)
    y_grid, x_grid = 20, 20

    # draw border
    pygame.draw.line(WIND, white, (0, 0), (W, 0))
    pygame.draw.line(WIND, white, (0, H - 1), (W, H - 1))
    pygame.draw.line(WIND, white, (0, 0), (0, H))
    pygame.draw.line(WIND, white, (W - 1, 0), (W - 1, H))
    for _ in range(W//GRID_W):
        pygame.draw.line(WIND, white, (0, y_grid), (W, y_grid))
        pygame.draw.line(WIND, white, (x_grid, 0), (x_grid, H))
        y_grid += GRID_H
        x_grid += GRID_W

    # display score
    score = len(snakeobj.body_lst) - 1
    f_score = pygame.font.SysFont('comicsans', 20)
    labelScore = f_score.render("Score: " + str(score), 1, white)
    lab_sco_x = Actual_W - labelScore.get_width()
    lab_sco_y = Actual_H - labelScore.get_height()
    WIND.blit(labelScore, (lab_sco_x, lab_sco_y))


def gen_food():
    randx = random.choice(range(0, W - W_FOOD, GRID_W))
    randy = random.choice(range(0, H - H_FOOD, GRID_H))
    return randx, randy


def collision(x1, y1, x2, y2):
    d = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
    if d == 0.0:
        return True
    return False


def collision_checks():
    global snakeobj, x_f, y_f
    h_x = snakeobj.head.x
    h_y = snakeobj.head.y

    # Check for food collision
    if collision(h_x, h_y, x_f, y_f):
        x_f, y_f = gen_food()
        snakeobj.add_body()

    # Check for snake body collision
    snake_body_coll(h_x, h_y)

    # Check for border collision
    is_border_hit(h_x, h_y)


def snake_body_coll(head_x, head_y):
    for part in snakeobj.body_lst[1:]:
        if collision(head_x, head_y, part.x, part.y):
            game_over()


def is_border_hit(x_, y_):
    x_check = x_ <= 0 - border or x_ >= W - border
    y_check = y_ <= 0 - border or y_ >= H - border
    if x_check or y_check:
        game_over()


def game_over():
    global WIND, score
    # Label Set up
    f_gameover = pygame.font.SysFont('comicsans', 50)
    labelGAMEOVER = f_gameover.render("GAMEOVER", 1, red)
    lab_go_x = (Actual_W // 2) - (labelGAMEOVER.get_width() // 2)
    lab_go_y = (Actual_H // 3) - (labelGAMEOVER.get_height() // 2)

    f_finalscore = pygame.font.SysFont('comicsans', 30)
    labelFinalScore = f_finalscore.render("Final Score: " + str(score), 1, white)
    lab_x = (Actual_W // 2) - (labelFinalScore.get_width() // 2)
    lab_y = ((Actual_W // 3) * 2) - (labelFinalScore.get_width() // 2)

    WIND.fill(black)
    WIND.blit(labelGAMEOVER, (lab_go_x, lab_go_y))
    WIND.blit(labelFinalScore, (lab_x, lab_y))
    pygame.display.update()
    time.sleep(6)


def main():
    global running, x, y, speed, x_f, y_f, border, W_SNAKE, H_SNAKE, timer, FPS
    while running:

        # Movement Var calculation
        old_dir = snakeobj.head.p_dir
        r_l_check = old_dir != "left" and old_dir != "right"
        u_d_check = old_dir != "down" and old_dir != "up"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                # Movement Checks
                direction = ""
                if event.key == pygame.K_RIGHT and r_l_check:
                    direction = "right"
                if event.key == pygame.K_LEFT and r_l_check:
                    direction = "left"
                if event.key == pygame.K_UP and u_d_check:
                    direction = "up"
                if event.key == pygame.K_DOWN and u_d_check:
                    direction = "down"
                if direction != "":
                    snakeobj.turn((snakeobj.head.x, snakeobj.head.y, direction))
                    direction = ""

        # Slow movement speed with timer
        if timer == 10:
            snakeobj.move()
            timer = 0
        timer += 1

        # All Collision Checks
        collision_checks()

        # Redraw images
        draw()

        # Update Screen and Run loop based on FPS
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
