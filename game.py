import pygame
import time
import random
import datetime
 
pygame.init()
pygame.font.init()

HEIGHT = 500
WIDTH = 500
SEG_SIZE = 10
time_zero = 0
stone_list = []

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)
now = datetime.datetime.now()

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,200,0)
ORANGE = (255,127,0)
YELLOW = (255,255,0)
CYAN = (50,50,255)
GREY = (100,100,100)

def compare(s):
    return int(s.split()[0])

def add_score(score, file):
    now = datetime.datetime.now()
    t = f'({str(now.hour)}:{str(now.minute)}:{(now.second)} {str(now.day)}.{str(now.month)}.{str(now.year)})'
    string = str(score) + " " + t + "\n"
    f = open(file, 'r')
    score_list = f.readlines()
    f.close()
    score_list.append(string)
    score_list = sorted(score_list, key = compare, reverse = True)
    f = open(file, 'w')
    for i in score_list:
        f.write(i)
    f.close()

def draw():
    screen.fill(GREEN)
    for i in Snake.tail:
        pygame.draw.rect(screen, YELLOW, [i[0], i[1], SEG_SIZE, SEG_SIZE])
    pygame.draw.rect(screen, YELLOW, [Snake.x, Snake.y, SEG_SIZE, SEG_SIZE])
    pygame.draw.rect(screen, RED, [Food.x, Food.y, SEG_SIZE, SEG_SIZE])
    if Bonus.flag:
        pygame.draw.rect(screen, Bonus.color, [Bonus.x, Bonus.y, SEG_SIZE, SEG_SIZE])
    for i in stone_list:
        pygame.draw.rect(screen, GREY, [i.x, i.y, i.size_x, i.size_y])
    
    string = font.render("Счёт: " + str(Snake.score), True, BLUE)
    screen.blit(string, [0, 0])
    pygame.display.update()


                


def end_screen():
    screen.fill(BLACK)
    string = font.render("Конец. Нажмите любую клавишу, чтобы выйти", True, RED)
    screen.blit(string, [0, HEIGHT / 3])
    string = font.render("Счёт: " + str(Snake.score), True, GREEN)
    screen.blit(string, [0, 0])
    pygame.display.update()

class Stone:
    def __init__(self, x, y, size_x = 2, size_y = 2):
        self.x = x
        self.y = y
        self.size_x = size_x * SEG_SIZE
        self.size_y = size_y * SEG_SIZE
        
    def is_inside_stone(x,y):
        for i in stone_list:
            if x >= i.x and x <= i.x + i.size_x - SEG_SIZE and y >= i.y and y <= i.y + i.size_y - SEG_SIZE:
                return True
        return False



def level_setting(num_stone, size, speed):
    for i in range(num_stone):
        x = (random.randint(0, WIDTH - size*SEG_SIZE) // SEG_SIZE) * SEG_SIZE
        y = (random.randint(0, HEIGHT - size*SEG_SIZE) // SEG_SIZE) * SEG_SIZE
        stone_list.append(Stone(x,y))
    Snake.speed_zero = speed

class Snake:
    x = (WIDTH // 2 // SEG_SIZE) * SEG_SIZE
    y = (HEIGHT // 2 // SEG_SIZE) * SEG_SIZE
    size = 1
    score = 0
    tail = []
    dx = 0
    dy = -SEG_SIZE
    speed_zero = 0
    dead = False
    def move():
        Snake.x += Snake.dx
        Snake.y += Snake.dy
        Snake.tail.append([Snake.x, Snake.y])
        while len(Snake.tail) > Snake.size:
            del Snake.tail[0]
    def slow():
        global time_zero
        Snake.speed_zero += (time.perf_counter() - time_zero) // 5 + 1
        Snake.speed_zero //= 2
        time_zero = time.perf_counter()

    def cut():
        Snake.size -= Snake.size // 3 

class Bonus:
    x = WIDTH + SEG_SIZE
    y = HEIGHT + SEG_SIZE
    flag = False
    time = time.perf_counter()
    color = 0

    def check():
        if not Bonus.flag and (time.perf_counter() - Bonus.time) > 10:
            Bonus.x = (random.randint(0, WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            Bonus.y = (random.randint(0, HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            while Stone.is_inside_stone(Bonus.x,Bonus.y):
                Bonus.x = (random.randint(0, WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
                Bonus.y = (random.randint(0, HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            Bonus.flag = True
            Bonus.color = random.choice((CYAN, ORANGE))
        if Bonus.x == Snake.x and Bonus.y == Snake.y:
            if Bonus.color == CYAN:
                Snake.slow()
            elif Bonus.color == ORANGE:
                Snake.cut()
            Bonus.time = time.perf_counter()
            Bonus.flag = False



class Food:
    x = WIDTH + SEG_SIZE
    y = HEIGHT + SEG_SIZE
    flag = False
    def check():
        if not Food.flag:
            Food.x = (random.randint(0, WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            Food.y = (random.randint(0, HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            while Stone.is_inside_stone(Food.x,Food.y):
                Food.x = (random.randint(0, WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
                Food.y = (random.randint(0, HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            Food.flag = True
        elif Food.x == Snake.x and Food.y == Snake.y:
            Food.x = (random.randint(0, WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            Food.y = (random.randint(0, HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            Snake.size += 1
            Snake.score += 1
        



# def Game():
#     Snake.dead = False
#     close = False
#     global time_zero
#     time_zero = time.perf_counter()
#     level_setting()
#     while close == False:
#         while Snake.dead == True:
#             screen.fill(BLACK)
#             string = font.render("Конец. Нажмите любую клавишу, чтобы выйти", True, red)
#             screen.blit(string, [0, HEIGHT / 3])
#             string = font.render("Счёт: " + str(Snake.score), True, green)
#             screen.blit(string, [0, 0])

#             pygame.display.update()

#             for event in pygame.event.get():
#                 if event.type == pygame.KEYDOWN:
#                     add_score(Snake.score)
#                     close = True
#                     Snake.dead = False

#         for e in pygame.event.get():
#             if e.type == pygame.QUIT:
#                 close = True
#             if e.type == pygame.KEYDOWN:
#                 if e.key == pygame.K_LEFT:
#                     Snake.dx = -SEG_SIZE
#                     Snake.dy = 0
#                 elif e.key == pygame.K_RIGHT:
#                     Snake.dx = SEG_SIZE
#                     Snake.dy = 0
#                 elif e.key == pygame.K_DOWN:
#                     Snake.dx = 0
#                     Snake.dy = SEG_SIZE
#                 elif e.key == pygame.K_UP:
#                     Snake.dx = 0
#                     Snake.dy = -SEG_SIZE
#         Snake.move()
#         if Snake.x < 0 or Snake.x > WIDTH or Snake.y < 0 or Snake.y > HEIGHT:
#             Snake.dead = True
#         if inside(Snake.x, Snake.y):
#             Snake.dead = True
#         for seg in Snake.tail[:-1]:
#             if seg == [Snake.x, Snake.y]:
#                 Snake.dead = True
#         Food.check()
#         Bonus.check()
#         draw()
#         clock.tick(Snake.speed_zero + (time.perf_counter() - time_zero) // 5)

#     pygame.quit()
#     quit()



# Game()