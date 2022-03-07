

import neat
import pygame
from sys import exit
import random

generation = 0
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
screen = pygame.display.set_mode((800, 800))
time = 0

class Snake:

    def __init__(self):

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.consecutive_turns = 0
        self.direction = 0
        self.past_direction = 0
        self.apples = 0
        self.x = 400
        self.y = 400
        self.surfaces = []
        self.head = pygame.Surface([10, 10])
        self.head.fill(self.color)
        self.is_alive = True
    
    def spawn_apple(self):
        self.apple = pygame.Surface([10, 10])
        self.ax = random.randint(1, 79) * 10
        self.ay = random.randint(1, 79) * 10
        self.apple.fill(self.color)
        while (self.ax, self.ay) in self.surfaces:
            self.ax = random.randint(1, 79) * 10
            self.ay = random.randint(1, 79) * 10
        
        #screen.blit(self.apple, (self.ax, self.ay))
    
    def get_data(self):
        self.adjacent = 0
        if (self.x - 1, self.y) in self.surfaces:
            self.adjacent += 1
        if (self.x + 1, self.y) in self.surfaces:
            self.adjacent += 1
        if (self.x, self.y - 1) in self.surfaces:
            self.adjacent += 1
        if (self.x, self.y + 1) in self.surfaces:
            self.adjacent += 1
        
        return [self.x - self.ax, self.y - self.ay, self.direction, self.past_direction, len(self.surfaces), self.adjacent,]
    
    def check_collision(self):
        
        if (self.x, self.y) in self.surfaces:
            self.is_alive = False
        if self.x <= 0 or self.x >= 800 or self.y <= 0 or self.y >= 800:
            self.is_alive = False
    
    def get_alive(self):
        return self.is_alive

    def get_reward(self):
        return self.apples
    
    def draw(self, screen):
        screen.blit(self.head, (self.x, self.y))
        #screen.blit(self.apple, (self.ax, self.ay))
    
    def get_apple_eaten(self):

        if (self.x, self.y) == (self.ax, self.ay):
            self.apples += 1
            self.spawn_apple()
        else:
            del self.surfaces[0]



def play_snake(genomes, config):

    nets = []
    snakes = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        snakes.append(Snake())

    pygame.init()
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    for snake in snakes:
        snake.spawn_apple()
    global generation 
    generation += 1
    time = 0

    while True:
        high_score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for snake in snakes:
                        snake.is_alive = False

        
        
        for index, snake in enumerate(snakes):
            output = nets[index].activate(snake.get_data())
            i = output.index(max(output))
            if i == 0:
                snake.direction = 0
            elif i == 1:
                snake.direction = 1
            elif i == 2:
                snake.direction = 2
            else:
                snake.direction = 3
        
        remain_snakes = 0
        for i, snake in enumerate(snakes):
            if snake.get_alive():
                remain_snakes += 1
                genomes[i][1].fitness += snake.get_reward()
        
        
        
        if remain_snakes == 0:
            break
        
        for snake in snakes:
            if snake.get_alive():
                snake.draw(screen)
        
        for snake in snakes:
            if snake.direction == 0 and snake.past_direction != 2: snake.y -= 10
            if snake.direction == 2 and snake.past_direction != 0: snake.y += 10
            if snake.direction == 3 and snake.past_direction != 1: snake.x -= 10
            if snake.direction == 1 and snake.past_direction != 3: snake.x += 10
            snake.past_direction = snake.direction

        for snake in snakes:
            snake.check_collision()
        #pygame.draw.rect(screen, white, pygame.Rect(x, y, 6, 6))

        screen.fill(black)
        
        for snake in snakes:
            snake.surfaces.append((snake.x, snake.y))
    
            for surface in snake.surfaces:
                if snake.get_alive():
                    screen.blit(pygame.Surface.copy(snake.head), surface)
                    screen.blit(snake.apple, (snake.ax, snake.ay))
            
            snake.get_apple_eaten()

        for snake in snakes:
            if snake.get_alive():
                if snake.apples > high_score:
                    high_score = snake.apples

        score = font.render(str(high_score), False, red)
        gen = font.render(str(generation), False, red)

        #screen.blit(head, (x, y))
        screen.blit(score, (400, 20))
        screen.blit(gen, (20, 20))
        pygame.display.update()
        clock.tick(120)
        for snake in snakes:
            if snake.apples <= 3 and time > 200:
                snake.is_alive = False 
        time += 1

                    

if __name__ == "__main__":

    config_path = "./PythonProjects/AISnake/config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(play_snake, 500)

