import pygame
import time
import random
import datetime
 
pygame.init()
pygame.font.init()

height = 500
width = 500
seg_size = 10
time_zero = 0
stone_list = []

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)
now = datetime.datetime.now()

black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,200,0)
orange = (255,127,0)
yellow = (255,255,0)
cyan = (50,50,255)
grey = (100,100,100)

def comp(s):
    return int(s.split()[0])

def add_score(sc):
    now = datetime.datetime.now()
    t = '(' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + ' ' + str(now.day) + '.' + str(now.month) + '.' + str(now.year) + ')'
    string = str(sc) + " " + t + "\n"
    f = open('score_C.txt', 'r')
    score_list = f.readlines()
    f.close()
    score_list.append(string)
    score_list = sorted(score_list, key = comp, reverse = True)
    f = open('score.txt', 'w')
    for i in score_list:
        f.write(i)
    f.close()

def draw():
    screen.fill(green)
    for i in Snake.tail:
        pygame.draw.rect(screen, yellow, [i[0], i[1], seg_size, seg_size])
    pygame.draw.rect(screen, yellow, [Snake.x, Snake.y, seg_size, seg_size])
    pygame.draw.rect(screen, red, [Food.x, Food.y, seg_size, seg_size])
    if Bonus.flag:
        pygame.draw.rect(screen, Bonus.color, [Bonus.x, Bonus.y, seg_size, seg_size])
    for i in stone_list:
        pygame.draw.rect(screen, grey, [i.x, i.y, i.size_x, i.size_y])
    
    string = font.render("Счёт: " + str(Snake.score), True, blue)
    screen.blit(string, [0, 0])
    pygame.display.update()

class Stone:
    def __init__(self, x, y, size_x = 2, size_y = 2):
        self.x = x
        self.y = y
        self.size_x = size_x * seg_size
        self.size_y = size_y * seg_size


def inside(x,y):
    for i in stone_list:
        if x >= i.x and x <= i.x + i.size_x - seg_size and y >= i.y and y <= i.y + i.size_y - seg_size:
            return True
    return False



def level():
    for i in range(3):
        x = (random.randint(0, width - 2*seg_size) // seg_size) * seg_size
        y = (random.randint(0, height - 2*seg_size) // seg_size) * seg_size
        stone_list.append(Stone(x,y))

class Snake:
    x = (width // 2 // seg_size) * seg_size
    y = (height // 2 // seg_size) * seg_size
    size = 1
    score = 0
    tail = []
    dx = 0
    dy = -seg_size
    speed_zero = 10
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
    x = width + seg_size
    y = height + seg_size
    flag = False
    time = time.perf_counter()
    color = 0

    def check():
        if not Bonus.flag and (time.perf_counter() - Bonus.time) > 10:
            Bonus.x = (random.randint(0, width - seg_size) // seg_size) * seg_size
            Bonus.y = (random.randint(0, height - seg_size) // seg_size) * seg_size
            while inside(Bonus.x,Bonus.y):
                Bonus.x = (random.randint(0, width - seg_size) // seg_size) * seg_size
                Bonus.y = (random.randint(0, height - seg_size) // seg_size) * seg_size
            Bonus.flag = True
            Bonus.color = random.choice((cyan, orange))
        if Bonus.x == Snake.x and Bonus.y == Snake.y:
            if Bonus.color == cyan:
                Snake.slow()
            elif Bonus.color == orange:
                Snake.cut()
            Bonus.time = time.perf_counter()
            Bonus.flag = False



class Food:
    x = width + seg_size
    y = height + seg_size
    flag = False
    def check():
        if not Food.flag:
            Food.x = (random.randint(0, width - seg_size) // seg_size) * seg_size
            Food.y = (random.randint(0, height - seg_size) // seg_size) * seg_size
            while inside(Food.x,Food.y):
                Food.x = (random.randint(0, width - seg_size) // seg_size) * seg_size
                Food.y = (random.randint(0, height - seg_size) // seg_size) * seg_size
            Food.flag = True
        elif Food.x == Snake.x and Food.y == Snake.y:
            Food.x = (random.randint(0, width - seg_size) // seg_size) * seg_size
            Food.y = (random.randint(0, height - seg_size) // seg_size) * seg_size
            Snake.size += 1
            Snake.score += 1
        



def Game():
    Snake.dead = False
    close = False
    global time_zero
    time_zero = time.perf_counter()
    level()
    while close == False:
        while Snake.dead == True:
            screen.fill(black)
            string = font.render("Конец. Нажмите любую клавишу, чтобы выйти", True, red)
            screen.blit(string, [0, height / 3])
            string = font.render("Счёт: " + str(Snake.score), True, green)
            screen.blit(string, [0, 0])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    add_score(Snake.score)
                    close = True
                    Snake.dead = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                close = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    Snake.dx = -seg_size
                    Snake.dy = 0
                elif e.key == pygame.K_RIGHT:
                    Snake.dx = seg_size
                    Snake.dy = 0
                elif e.key == pygame.K_DOWN:
                    Snake.dx = 0
                    Snake.dy = seg_size
                elif e.key == pygame.K_UP:
                    Snake.dx = 0
                    Snake.dy = -seg_size
        Snake.move()
        if Snake.x < 0 or Snake.x > width or Snake.y < 0 or Snake.y > height:
            Snake.dead = True
        if inside(Snake.x, Snake.y):
            Snake.dead = True
        for seg in Snake.tail[:-1]:
            if seg == [Snake.x, Snake.y]:
                Snake.dead = True
        Food.check()
        Bonus.check()
        draw()
        clock.tick(Snake.speed_zero + (time.perf_counter() - time_zero) // 5)

    pygame.quit()
    quit()



Game()