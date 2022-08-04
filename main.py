import pygame
import sys
from boid import Boid
from random import randint as ri
sys.path.append("..")
from pygame_projects.vector import Vector
from predator import Predator

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("boids")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BG = (60, 45, 65)

FPS = 60
NUM_BOIDS = 50

def main():
    clock = pygame.time.Clock()
    run = True
    boids = []

    predator = Predator(WIDTH//2, HEIGHT//2, 15)

    for i in range(NUM_BOIDS):
        boids.append(Boid(ri(0, WIDTH), ri(0, HEIGHT), 5))

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()

        mousex, mousey = pygame.mouse.get_pos()
        mouse = Vector(mousex, mousey)

        predator.move(keys_pressed)

        for boid in boids:
            #if Vector.static_dist(boid.pos, predator.pos) < 150 and boid.witin_bounds: #and pygame.mouse.get_pressed()[0] == 1:
            if Vector.static_dist(boid.pos, mouse) < 150 and boid.witin_bounds and pygame.mouse.get_pressed()[0] == 1:
                flee = boid.flee(mouse)
                flee.mult(5)
                boid.apply_force(flee)
            if pygame.mouse.get_pressed()[2] == 1:
                seek = boid.seek(mouse)
                boid.apply_force(seek)

            boid.update()
            boid.flock(boids)
            boid.wrap_around(WIDTH, HEIGHT)
            #boid.wrap_around(WIDTH, HEIGHT)

        draw_window(boids, predator)

def boids_avg_pos(boids):
    avg_pos = Vector(0, 0)
    count = 0
    for boid in boids:
        avg_pos.add(boid.pos)
        count += 1

    avg_pos.div(count)
    return avg_pos

def draw_window(boids, predator):
    WIN.fill(BG)

    #avg_pos = boids_avg_pos(boids)
    #pygame.draw.circle(WIN, (235, 64, 52), (avg_pos.x, avg_pos.y), 15)
    #predator.show(WIN)

    for boid in boids:
        boid.show(WIN)

    pygame.display.update()


if __name__ == "__main__":
    main()
