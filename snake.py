#import neat
import pygame
from sys import exit
import random

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Snake")

    font = pygame.font.Font(None, 30)

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    direction = ""
    past_direction = ""
    clock = pygame.time.Clock()
    
    apples = 0
    x = 400
    y = 400
    surfaces = []
    head = pygame.Surface([10, 10])
    head.fill(white)

    def spawn_apple():
        global apple, ax, ay
        apple = pygame.Surface([10, 10])
        ax = random.randint(1, 79) * 10
        ay = random.randint(1, 79) * 10
        apple.fill(red)
        while (ax, ay) in surfaces:
            ax = random.randint(1, 79) * 10
            ay = random.randint(1, 79) * 10
        
        screen.blit(apple, (ax, ay))

    spawn_apple()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and past_direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and past_direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and past_direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and past_direction != "LEFT":
                    direction = "RIGHT"
        
        if direction == "UP": y -= 10
        if direction == "DOWN": y += 10
        if direction == "LEFT": x -= 10
        if direction == "RIGHT": x += 10
        past_direction = direction
        #pygame.draw.rect(screen, white, pygame.Rect(x, y, 6, 6))
        
        if (x, y) in surfaces:
            print(f"FINAL SCORE: {apples}")
            exit()
        if x == 0 or x == 800 or y == 0 or y == 800:
            print(f"FINAL SCORE: {apples}")
            exit()

        screen.fill(black)
        surfaces.append((x, y))
        
        #print(surfaces)
        for surface in surfaces:
            screen.blit(pygame.Surface.copy(head), surface)

        if (x, y) == (ax, ay):
            apples += 1
            spawn_apple()
        else:
            del surfaces[0]
            screen.blit(apple, (ax, ay))

        score = font.render(str(apples), False, red)

        screen.blit(head, (x, y))
        screen.blit(score, (400, 20))
        pygame.display.update()
        clock.tick(15)


                    

if __name__ == "__main__":

    main()
