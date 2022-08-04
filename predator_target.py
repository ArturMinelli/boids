import time

import neat
import pygame
from random import randint as ri
from pygame_projects.vector import Vector
from predator import  Predator
import pickle
import os

pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("setup")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BG = (60, 50, 65)

FPS_TRAIN = 600
FPS_TEST = 60

class Target:
    def __init__(self, x, y, r):
        self.pos = Vector(x, y)
        self.vel = Vector.static_random_dir()
        self.vel.mult(4)
        self.r = r

    def update(self):
        self.pos.add(self.vel)

    def edges(self):
        if self.pos.x + self.r > WIDTH:
            self.pos.x = WIDTH - self.r - 1
            self.vel.x *= -1
        if self.pos.x - self.r < 0:
            self.pos.x = self.r + 1
            self.vel.x *= -1
        if self.pos.y + self.r > HEIGHT:
            self.pos.y = HEIGHT - self.r - 1
            self.vel.y *= -1
        if self.pos.y - self.r < 0:
            self.pos.y = self.r + 1
            self.vel.y *= -1

    def show(self, win):
        pygame.draw.circle(win, (255, 54, 54), (self.pos.x, self.pos.y), self.r//15)
        pygame.draw.circle(win, (255, 54, 54), (self.pos.x, self.pos.y), self.r, self.r//15)


def draw_window(predators, target):
    WIN.fill(BG)

    target.show(WIN)

    for predator in predators:
        predator.show(WIN)

    pygame.display.update()


def train_AI(genome_list, config):
    clock = pygame.time.Clock()

    predators = []
    genomes = []
    nets = []

    target = Target(WIDTH/2, HEIGHT/2, 100)

    for i in range(len(genome_list)):
        predators.append(Predator(ri(0, WIDTH), ri(0, HEIGHT), 10))
        genomes.append(genome_list[i][1])
        nets.append(neat.nn.FeedForwardNetwork.create(genomes[i], config))


    run = True
    start_time = time.time()
    while run:
        clock.tick(FPS_TRAIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    train_AI()

        keys_pressed = pygame.key.get_pressed()

        for i, predator in enumerate(predators):
            predator.move_AI(nets[i], target)
            #predator.move(keys_pressed)
            predator.edges(WIDTH, HEIGHT)
            if Vector.static_dist(predator.pos, target.pos) < target.r:
                predator.score += 0.3

        target.update()
        target.edges()

        current_time = time.time()
        if current_time - start_time > 3:
            calc_fitness(predators, genomes)
            break

        draw_window(predators, target)

def test_AI(net):
    clock = pygame.time.Clock()

    predators = []

    target = Target(WIDTH/2, HEIGHT/2, 100)

    predators.append(Predator(WIDTH//2, HEIGHT//2, 10))

    run = True
    while run:
        clock.tick(FPS_TEST)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    train_AI()

        keys_pressed = pygame.key.get_pressed()

        for i, predator in enumerate(predators):
            predator.move_AI(net, target.pos)
            #predator.move(keys_pressed)
            predator.edges(WIDTH, HEIGHT)
            if Vector.static_dist(predator.pos, target.pos) < target.r:
                predator.score += 0.3

        target.update()
        target.edges()

        draw_window(predators, target)

def calc_fitness(predators, genomes):
    for i, genome in enumerate(genomes):
        genome.fitness += predators[i].score



def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        if genome.fitness is None:
            genome.fitness = 0

    train_AI(genomes, config)


def run(config):
    #p = neat.Population(config)
    p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-99")

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(20))

    winner = p.run(eval_genomes, 100)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


    print('\nBest genome:\n{!s}'.format(winner))


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    test_AI(winner_net)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    #run(config)
    test_best_network(config)