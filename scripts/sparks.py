import pygame, math

'''Taken from: https://www.youtube.com/watch?v=wNMRq_uoWM0'''
class Spark():
    def __init__(self, pos, angle, speed, colour, scale=1):
        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.colour = colour
        self.alive = True

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    def update(self, dt):
        movement = self.calculate_movement(dt)
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]

        self.speed -= 0.5

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf):
        if self.alive:
            points = [
                [self.pos[0] + math.cos(self.angle) * self.speed * self.scale, self.pos[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.pos[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.pos[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.pos[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.pos[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.pos[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.pos[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                ]
            pygame.draw.polygon(surf, self.colour, points)