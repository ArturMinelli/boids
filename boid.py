import pygame.draw

from pygame_projects.vector import Vector

class Boid:
    def __init__(self, x, y, r):
        self.pos = Vector(x, y)
        self.vel = Vector.static_random_dir()
        self.acc = Vector(0, 0)
        self.r = r
        self.max_speed = 5
        self.max_force = 0.1
        self.fov = 135
        self.witin_bounds = True

    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(self.max_speed)
        self.pos.add(self.vel)
        self.acc.mult(0)

    def seek(self, target):
        desire = Vector.static_sub(target, self.pos)
        desire.setMag(self.max_speed)
        steering = Vector.static_sub(desire, self.vel)
        steering.limit(self.max_force)

        return steering

    def flee(self, target):
        flee = self.seek(target)
        flee.mult(-1)

        return flee

    def align(self, boids):
        steering = Vector(0, 0)
        align_radius = 100
        count = 0
        for boid in boids:
            vector_to_boid = Vector.static_sub(boid.pos, self.pos)
            dist = vector_to_boid.mag()
            angle_to_boid = Vector.static_angle_between(self.vel, vector_to_boid)
            if dist < align_radius and boid is not self and angle_to_boid < self.fov:
                steering.add(boid.vel)
                count += 1

        if count != 0:
            steering.div(count)
            steering.setMag(self.max_speed)
            steering.sub(self.vel)
            steering.limit(self.max_force)

        return steering

    def separate(self, boids):
        steering = Vector(0, 0)
        count = 0
        separation_radius = 50
        for boid in boids:
            vector_to_boid = Vector.static_sub(boid.pos, self.pos)
            angle_to_boid = Vector.static_angle_between(self.vel, vector_to_boid)
            dist = vector_to_boid.mag()
            if dist < separation_radius and angle_to_boid < self.fov and boid is not self:
                vector_to_boid.setMag(self.max_speed)
                vector_to_boid.mult(-1)
                vector_to_boid.div(dist)
                steering.add(vector_to_boid)
                count += 1

        if count > 0:
            steering.div(count)
            steering.limit(self.max_force)

        return steering

    def cohesion(self, boids):
        steering = Vector(0, 0)
        cohesion_radius = 100
        count = 0
        for boid in boids:
            vector_to_boid = Vector.static_sub(boid.pos, self.pos)
            dist = vector_to_boid.mag()
            angle_to_boid = Vector.static_angle_between(self.vel, vector_to_boid)
            if dist < cohesion_radius and boid is not self and angle_to_boid < self.fov:
                steering.add(boid.pos)
                count += 1

        if count != 0:
            steering.div(count)
            steering.sub(self.pos)
            steering.setMag(self.max_speed)
            steering.sub(self.vel)
            steering.limit(self.max_force)

        return steering

    def flock(self, boids):
        align = self.align(boids)
        cohesion = self.cohesion(boids)
        separate = self.separate(boids)
        separate.mult(1.5)

        self.apply_force(align)
        self.apply_force(cohesion)
        self.apply_force(separate)

    def apply_force(self, force):
        self.acc.add(force)

    def wrap_around(self, width, height):
        if self.pos.x - self.r > width: self.pos.x = -self.r + 1
        if self.pos.x + self.r < 0: self.pos.x = width + self.r - 1
        if self.pos.y - self.r > height: self.pos.y = -self.r + 1
        if self.pos.y + self.r < 0: self.pos.y = height + self.r - 1

    def edges(self, width, height):
        left_wall_dist = abs(self.pos.x)
        right_wall_dist = abs(self.pos.x - width)
        top_wall_dist = abs(self.pos.y)
        bottom_wall_dist = abs(self.pos.y - height)

        repulsion_distance = 15

        if left_wall_dist < repulsion_distance:
            self.vel.x += 0.45
        if right_wall_dist < repulsion_distance:
            self.vel.x -= 0.45

        if top_wall_dist < repulsion_distance:
            self.vel.y += 0.45
        if bottom_wall_dist < repulsion_distance:
            self.vel.y -= 0.45

        self.witin_bounds = True
        for wall_dist in [left_wall_dist, right_wall_dist, top_wall_dist, bottom_wall_dist]:
            if wall_dist < repulsion_distance + 45:
                self.witin_bounds = False


    def show(self, win):
        direction = self.vel.copy()
        direction.setMag(self.r * 3)
        direction.add(self.pos)

        pygame.draw.line(win, (255, 255, 255), (self.pos.x, self.pos.y), (direction.x, direction.y))
        pygame.draw.circle(win, (0, 255, 150), (self.pos.x, self.pos.y), self.r)
        pygame.draw.circle(win, (0, 255, 150), (direction.x, direction.y), self.r//2.3)

def p5_map(n, start1, start2, stop1, stop2):
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2