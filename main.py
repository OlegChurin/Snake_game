import game
import pygame
import time

Snake = game.Snake
screen = game.screen
font = game.font
HEIGHT = game.HEIGHT
WIDTH = game.WIDTH
SEG_SIZE = game.SEG_SIZE


def Start():
    Snake.dead = False
    close = False
    global time_zero
    time_zero = time.perf_counter()

    non_started = True
    while non_started:
        screen.fill(game.BLACK)
        string = font.render("Нажмите на клавишу A, B, C, D или E для выбора уровня", True, game.RED)
        screen.blit(string, [0, HEIGHT / 3])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game.level_setting(1,2,5)
                    result_file = 'score_A.txt'
                    non_started = False
                elif event.key == pygame.K_b:
                    game.level_setting(2,2,5)
                    result_file = 'score_B.txt'
                    non_started = False
                elif event.key == pygame.K_c:
                    game.level_setting(3,2,10)
                    result_file = 'score_C.txt'
                    non_started = False
                elif event.key == pygame.K_d:
                    game.level_setting(4,3,10)
                    result_file = 'score_D.txt'
                    non_started = False
                elif event.key == pygame.K_e:
                    game.level_setting(0,2,20)
                    result_file = 'score_E.txt'
                    non_started = False
    while close == False:
        while Snake.dead == True:
            game.end_screen()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    game.add_score(Snake.score, result_file)
                    close = True
                    Snake.dead = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                close = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    Snake.dx = -SEG_SIZE
                    Snake.dy = 0
                elif e.key == pygame.K_RIGHT:
                    Snake.dx = SEG_SIZE
                    Snake.dy = 0
                elif e.key == pygame.K_DOWN:
                    Snake.dx = 0
                    Snake.dy = SEG_SIZE
                elif e.key == pygame.K_UP:
                    Snake.dx = 0
                    Snake.dy = -SEG_SIZE
        Snake.move()
        if Snake.x < 0 or Snake.x > WIDTH or Snake.y < 0 or Snake.y > HEIGHT:
            Snake.dead = True
        if game.Stone.is_inside_stone(Snake.x, Snake.y):
            Snake.dead = True
        for seg in Snake.tail[:-1]:
            if seg == [Snake.x, Snake.y]:
                Snake.dead = True
        game.Food.check()
        game.Bonus.check()
        game.draw()
        game.clock.tick(Snake.speed_zero + (time.perf_counter() - time_zero) // 5)

    pygame.quit()
    quit()



Start()